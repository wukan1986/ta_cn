import pathlib

from itertools import product

import pandas as pd
import parmap
from loguru import logger

from best_practices.utils import func_load_calc_save, dataframe_save, timer, func_load_parquet

# 行范围，字符串，只用在文件名上
# 分钟数据太大，可改为按月划分
RANGE_I = pd.date_range('2020-01-01', '2022-12-31', freq='Y')
RANGE_I = [f'{i:%Y}' for i in RANGE_I]

# 列范围，字符串，只用在文件名上
# 横向10组在数据量大时也比较慢，可改为20组，50组等
RANGE_J = [f'{i:02d}' for i in range(10)]

# 数据源路径
PATH_STEP0_INPUT1 = r'D:\data\jqresearch\get_price_stock_daily'
PATH_STEP0_INPUT2 = r'D:\data\jqresearch\get_price_stock_factor'
PATH_STEP0_INPUT3 = r'D:\data\jqresearch\get_extras_stock_is_st'
# 中间过程路径。可以考虑这部分保存到共享内存或内存盘中，加快速度
PATH_STEP0_OUTPUT = r'M:\data3\step0'
PATH_STEP1_OUTPUT = r'M:\data3\step1'


def func_prepare(df, i, j):
    """准备工作。从外部导入数据后，对数据做一些准备工作

    Parameters
    ----------
    df
    i
    j

    Returns
    -------

    """
    # 统一表头，防止不同数据源要分别写代码
    df.rename(columns={'code': 'asset', 'time': 'date', 'money': 'amount'}, inplace=True)
    # 不做科创板，不做创业板
    df = df[~df['asset'].str.startswith(('688', '300'))].copy()
    # 先转类型
    df['asset'] = df['asset'].astype('category')
    # 只转换小样本，速度更快
    to_replace = {r'(\d+)\.XSHG': r'\1.SH', r'(\d+)\.XSHE': r'\1.SZ'}
    cat = df['asset'].cat.categories
    mapping = pd.Series(cat, index=cat).replace(to_replace, regex=True)
    df['asset'] = df['asset'].cat.rename_categories(mapping.to_dict())

    # 过滤停牌。计算技术指标和和横截面时会剔除停牌，但计算板块和指数时，停牌也参与计算
    df = df[df['paused'] == 0].copy()

    # # 用数字节约内存
    # df[AXIS_I] = int(i)
    # # [5: 6]一位用来当关键字，数据量大就用两位[4:6]
    # df[AXIS_J] = df['asset'].str[5:6].astype(int)
    # # set_index处理后，index中的类型变成了uint64,很无语
    # # df[AXIS_I] = df[AXIS_I].astype(np.uint16)  # 请按数据情况填写，因为可能是2022年，又有可能是202211月，也可能是20221121日
    # # df[AXIS_J] = df[AXIS_J].astype(np.uint8)  # 划分数量一般小时CPU真核数量

    # 内存优化
    df['paused'] = df['paused'].astype(bool)

    # 整理排序，加入了两个特殊列, 这样在后面的文件划分时处理更方便
    # df = df.set_index(['asset', 'date', AXIS_I, AXIS_J]).sort_index()
    df = df.set_index(['asset', 'date']).sort_index()

    return df


def func_is_st(df: pd.DataFrame):
    df = df.stack(dropna=True)
    df.name = 'is_st'
    df.index.names = ['time', 'code']
    df = df.reset_index()
    return df


@timer
def step0():
    """计算技术指标，并提取用来算横截面的字段"""

    ii = RANGE_I  # 年份
    jj = ['*']  # 品种
    parmap.map(func_load_calc_save,
               product(ii, jj),
               load_func=func_load_parquet, load_kwargs=
               {
                   'path': [PATH_STEP0_INPUT1, PATH_STEP0_INPUT2, PATH_STEP0_INPUT3],
                   'pattern': ['{0}*', '{0}*', '{0}*'],
                   'axis': [0, 0, 0],
                   'func': [None, None, func_is_st],
                   # 源数据来自聚宽，股票代码和时间如下
                   'on': [['code', 'time'], ['code', 'time'], ['code', 'time']],
                   'index': [False, False, False],
               },
               calc_func=func_prepare, calc_args=[],
               save_func=dataframe_save, save_args=
               [
                   # 这里没有按品种分别保存
                   {'split_axis': None, 'path': PATH_STEP0_OUTPUT, 'exclude': []},  # 上流输入`三`型，输出转`田`型
               ],
               pm_processes=len(ii),
               pm_parallel=True)


@timer
def step1():
    """合并多个parquet文件，因为在polars中不支持分类变量合并加载，所以在这进行合并，否则是可以不需要此步"""
    path1 = pathlib.Path(PATH_STEP0_OUTPUT)
    path2 = pathlib.Path(PATH_STEP1_OUTPUT)
    path2.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(path1)  # 读数文件夹
    df.to_parquet(path2 / 'data.parquet', compression='zstd')


if __name__ == '__main__':
    # 原始数据合并
    step0()
    # 再次合并数据
    step1()

    logger.info('done')
