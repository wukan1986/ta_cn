import pathlib

import polars as pl
from loguru import logger
from polars import LazyFrame
from talib import *

from best_practices.utils import pl_np_wraps
from ta_cn import EPSILON
from ta_cn.tdx.logical import CROSS
from ta_cn.tdx.over_bought_over_sold import KDJ
from ta_cn.tdx.reference import BARSLASTCOUNT
from ta_cn.tdx.statistics import limit_count
from ta_cn.wq.cross_sectional import rank
from ta_cn.wq.time_series import ts_returns, ts_rank


def calc_col(df: LazyFrame) -> LazyFrame:
    """整列运算，不用groupby"""

    # 第一阶段，只利用原字段
    df = df.with_columns([

        (pl.col('high') + pl.col('low')).alias('mid_price'),

        # 需要传入到talib,所以先不转float32
        (pl.col('open') * pl.col('factor')).alias('open_adj'),
        (pl.col('high') * pl.col('factor')).alias('high_adj'),
        (pl.col('low') * pl.col('factor')).alias('low_adj'),
        (pl.col('close') * pl.col('factor')).alias('close_adj'),

        (pl.col('close') >= pl.col('high_limit') - EPSILON).alias('涨停'),
        (pl.col('high') >= pl.col('high_limit') - EPSILON).alias('曾涨停'),
        (pl.col('close') <= pl.col('low_limit') + EPSILON).alias('跌停'),
        (pl.col('low') <= pl.col('low_limit') + EPSILON).alias('曾跌停'),

        (pl.col('low') >= pl.col('high_limit') - EPSILON).alias('一字板'),

        (pl.col('close') / pl.col('pre_close') - 1).cast(pl.Float32).alias('pct')
    ])

    # 第二阶段，利用新字段
    df = df.with_columns([

        (pl.col('涨停') & (pl.col('high') > pl.col('low'))).alias('T字板'),
    ])

    return df


def calc_ts(df) -> LazyFrame:
    """时序方向上计算，按股票分组。注意时序有先后顺序"""
    # 第一阶段
    df = df.with_columns([
        # 收益率标签
        pl.col('close_adj').pct_change(1).shift(-1).alias('returns_1'),
        pl.col('close_adj').pct_change(5).shift(-5).alias('returns_5'),
        pl.col('close_adj').pct_change(10).shift(-10).alias('returns_10'),

        pl.col('close_adj').pct_change(1).alias('mom_1'),
        pl.col('close_adj').pct_change(5).alias('mom_5'),
        pl.col('close_adj').pct_change(10).alias('mom_10'),
        #
        *[pl.col('CLOSE').pct_change(i).alias(f'ROCP_{i}') for i in (1, 3, 5, 10, 20, 60)],

        pl.col('close_adj').map(lambda x: RSI(x, 6)).cast(pl.Float32).alias('rsi_6'),
        pl.col('close_adj').map(lambda x: RSI(x, 12)).cast(pl.Float32).alias('rsi_12'),
        pl.col('close_adj').map(lambda x: RSI(x, 24)).cast(pl.Float32).alias('rsi_24'),

        pl.col('close_adj').map(lambda x: STDDEV(x, 20)).cast(pl.Float32).alias('std'),
        pl.col('close_adj').map(lambda x: ROCP(x, 10)).cast(pl.Float32).alias('rocp'),

        pl.col('amount').map(lambda x: pl_np_wraps(ts_returns)(x, 1)).alias('amount_ratio'),

        pl.col('close_adj').map(lambda x: pl_np_wraps(ts_rank)(x, 10)).alias('收盘价10日排序'),
        pl.col('close_adj').map(lambda x: pl_np_wraps(ts_rank)(x, 20)).alias('收盘价20日排序'),

        # 多输入，单输出
        pl.map(['close_adj', 'volume'], lambda x: OBV(*x)).cast(pl.Float32).alias('obv'),
        pl.map(['high_adj', 'low_adj', 'close_adj'], lambda x: CCI(*x, 14)).cast(pl.Float32).alias('cci'),
        pl.map(['high_adj', 'low_adj', 'close_adj'], lambda x: WILLR(*x, 6)).cast(pl.Float32).alias('wr_6'),
        pl.map(['high_adj', 'low_adj', 'close_adj'], lambda x: WILLR(*x, 10)).cast(pl.Float32).alias('wr_10'),
        pl.map(['high_adj', 'low_adj', 'close_adj'], lambda x: NATR(*x, 14)).cast(pl.Float32).alias('atr_14'),

        # 这个为何严重拖慢速度？多线程优势为何没了？
        pl.col('涨停').map(lambda x: pl_np_wraps(BARSLASTCOUNT)(x)).alias('连板'),
    ])

    # 第二阶段
    df = df.with_columns([
        pl.map(['sma_5', 'sma_10'], lambda x: pl_np_wraps(CROSS)(*x)).alias('MA金叉'),
    ])

    # 多输出
    df = df.hstack(
        pl.DataFrame([
            *MACDEXT(df["close_adj"],
                     fastperiod=12, fastmatype=1,
                     slowperiod=26, slowmatype=1,
                     signalperiod=9, signalmatype=1),
            *BBANDS(df['close_adj'],
                    timeperiod=20, nbdevup=2, nbdevdn=2, matype=0),
            *pl_np_wraps(KDJ, 3, 3)(df['high_adj'], df['low_adj'], df['close_adj'], 9, 3, 3),
            *pl_np_wraps(limit_count, 1, 2)(df['涨停'], 2),
        ],
            columns=[
                "macd", "macdsignal", "macdhist",
                "upperband", "middleband", "lowerband",
                "kdj_k", "kdj_d", "kdj_j",
                "N天", "M板",
            ]
        )
    )

    return df


def calc_cs(df: LazyFrame) -> LazyFrame:
    """截面处理"""

    df = df.with_columns([
        pl.col('close').map(lambda x: pl_np_wraps(rank)(x)).alias('close_rank'),
    ])

    # 目前没有行情业数据，只能模拟行业分组
    df = df.with_columns([
        (pl.col('close_rank') * 10 // 2).cast(pl.Int8).alias('industry'),
    ])

    df = df.with_columns([
        pl.col('returns_1').map(lambda x: pl_np_wraps(rank)(x)).alias('label_1'),
        pl.col('returns_5').map(lambda x: pl_np_wraps(rank)(x)).alias('label_5'),
        pl.col('returns_10').map(lambda x: pl_np_wraps(rank)(x)).alias('label_10'),
    ])

    return df


def calc_cs2(df: LazyFrame):
    """行业中性处理演示"""
    df = df.with_columns([
        pl.col('amount').map(lambda x: pl_np_wraps(rank)(x)).alias('amount_rank'),

    ])
    return df


if __name__ == '__main__':
    PATH_STEP1_OUTPUT = r'M:\data3\step1'
    PATH_STEP2_OUTPUT = r'M:\data3\step2'

    # 路径准备
    PATH_STEP1_OUTPUT = pathlib.Path(PATH_STEP1_OUTPUT)
    PATH_STEP2_OUTPUT = pathlib.Path(PATH_STEP2_OUTPUT)
    PATH_STEP2_OUTPUT.mkdir(parents=True, exist_ok=True)

    logger.info('开始 数据加载')
    df = pl.read_parquet(PATH_STEP1_OUTPUT / '*.parquet', use_pyarrow=False, memory_map=True)
    # 调整表头顺序，方便观察
    df = df.select([
        pl.col(['asset', 'date']),
        pl.all().exclude(['asset', 'date'])
    ])
    print(df.head())
    logger.info('开始 列计算')
    df = calc_col(df)

    logger.info('开始 时序计算')
    # 计算时序指标时date一定要保证顺序
    df = df.sort(by=['asset', 'date'])
    df = df.groupby(by=['asset']).apply(calc_ts)

    logger.info('开始 截面计算')
    # 排序后的数据groupby会更快
    df = df.sort(by=['date', 'asset'])
    df = df.groupby(by=['date']).apply(calc_cs)

    logger.info('开始 行业处理')
    df = df.groupby(by=['date', 'industry']).apply(calc_cs2)

    logger.info('开始 保存')
    # gzip格式耗时长，压缩率也没有明显提高, zstd格式好像更合适
    df.write_parquet(PATH_STEP2_OUTPUT / 'feature.parquet', compression='zstd')

    logger.info('完成')
    print(df.tail())
