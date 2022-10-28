"""
这里的时序和截面是已经分组过后，已经变成了一维，所以直接使用一维函数即可
"""

import ta_cn

ta_cn.numba_cache = True

import numpy as np
import pandas as pd

from ta_cn.tdx.reference import BARSLASTCOUNT
from ta_cn.wq.cross_sectional import rank
from ta_cn.wq.time_series import ts_rank
from ta_cn.wq.time_series import ts_returns
from ta_cn.tdx.statistics import limit_count
from ta_cn.tdx.over_bought_over_sold import KDJ
from ta_cn.tdx.logical import CROSS
from .utils import AXIS_I, AXIS_J
from talib import *

EPSILON = ta_cn.EPSILON


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
    # 先转类型
    df['asset'] = df['asset'].astype('category')
    # 只转换小样本，速度更快
    to_replace = {r'(\d+)\.XSHG': r'\1.SH', r'(\d+)\.XSHE': r'\1.SZ'}
    df['asset'].cat.categories = pd.Series(df['asset'].cat.categories).replace(to_replace, regex=True)

    # 过滤停牌。计算技术指标和和横截面时会剔除停牌，但计算板块和指数时，停牌也参与计算
    df = df[df['paused'] == 0].copy()

    # 用数字节约内存
    df[AXIS_I] = int(i)
    # [5: 6]一位用来当关键字，数据量大就用两位[4:6]
    df[AXIS_J] = df['asset'].str[5:6].astype(int)

    # 内存优化
    df['paused'] = df['paused'].astype(bool)
    df[AXIS_I] = df[AXIS_I].astype(np.uint16)  # 请按数据情况填写
    df[AXIS_J] = df[AXIS_J].astype(np.uint8)

    # 整理排序
    df = df.set_index(['asset', 'date']).sort_index()

    return df


def calc_col(df: pd.DataFrame):
    """没有分组的原始数据直接计算

    只在开始时调用几次，例如，三年文件，按年加载后，那么只调用3次
    """
    # 与时序和横截面都无关的直接计算
    df['mid_price'] = (df['high'] + df['low']) / 2.0

    # 后复权
    df['open_adj'] = df['open'] * df['factor']
    df['high_adj'] = df['high'] * df['factor']
    df['low_adj'] = df['low'] * df['factor']
    df['close_adj'] = df['close'] * df['factor']

    df['涨停'] = df['close'] >= df['high_limit'] - EPSILON
    df['曾涨停'] = df['high'] >= df['high_limit'] - EPSILON
    df['跌停'] = df['close'] <= df['low_limit'] + EPSILON
    df['曾跌停'] = df['low'] <= df['low_limit'] + EPSILON

    df['一字板'] = df['low'] >= df['high_limit'] - EPSILON
    df['T字板'] = df['涨停'] & (df['high'] > df['low'])

    # 涨幅，没有乘100%
    df['pct'] = df['close'] / df['pre_close'] - 1.0
    return df


def calc_ts(df: pd.DataFrame):
    """按asset分组后，得到时序每列，然后应用相应计算函数

    多少列，多少支股票就调用多少次，4000支就调用4000次
    """
    # 计算指标，输入已经按股票分好了，所以直接调用talib更快

    # 收益率标签，注意：由于移动了位置，这是未来数据，只能做标签用
    df['returns_1'] = ts_returns(df['close_adj'], -1)
    df['returns_5'] = ts_returns(df['close_adj'], -5)
    df['returns_10'] = ts_returns(df['close_adj'], -10)

    # SMA
    df['sma_5'] = SMA(df['close_adj'], timeperiod=5)
    df['sma_10'] = SMA(df['close_adj'], timeperiod=10)
    df['sma_20'] = SMA(df['close_adj'], timeperiod=20)
    df['sma_60'] = SMA(df['close_adj'], timeperiod=60)
    df['sma_120'] = SMA(df['close_adj'], timeperiod=120)
    df['sma_240'] = SMA(df['close_adj'], timeperiod=240)

    # MACD，以前是单休，所以12天
    df['macd'], df['macdsignal'], df['macdhist'] = MACDEXT(df['close_adj'],
                                                           fastperiod=12, fastmatype=1,
                                                           slowperiod=26, slowmatype=1,
                                                           signalperiod=9, signalmatype=1)

    ##
    df['bbu'], _, df['bbl'] = BBANDS(df['close_adj'],
                                     timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

    df['std'] = STDDEV(df['close_adj'], timeperiod=20)

    # 要不要加30
    df['obv'] = OBV(df['close_adj'], df['volume'])

    ##
    df['rsi_6'] = RSI(df['close_adj'], timeperiod=6)
    df['rsi_12'] = RSI(df['close_adj'], timeperiod=12)
    df['rsi_24'] = RSI(df['close_adj'], timeperiod=24)

    df['wr_6'] = WILLR(df['high_adj'], df['low_adj'], df['close_adj'], timeperiod=6)
    df['wr_10'] = WILLR(df['high_adj'], df['low_adj'], df['close_adj'], timeperiod=10)

    ##
    df['kdj_k'], df['kdj_d'], df['kdj_j'] = KDJ(df['high_adj'], df['low_adj'], df['close_adj'], 9, 3, 3)

    df['roc'] = ROC(df['close_adj'], timeperiod=10)
    df['cci'] = CCI(df['high_adj'], df['low_adj'], df['close_adj'], timeperiod=14)

    # ATR, 要不要换成NATR
    df['atr_14'] = ATR(df['high_adj'], df['low_adj'], df['close_adj'], timeperiod=14)

    # 成交额与昨成交额比
    df['amount_ratio'] = ts_returns(df['amount'], 1)

    # rank排序
    # 不直接使用move_rank是因为有效长度不足会报错，原范围是-1至1，想调整成0至1
    df['收盘价10日排序'] = ts_rank(df['close_adj'], 10)
    df['收盘价20日排序'] = ts_rank(df['close_adj'], 20)

    df['连板'] = BARSLASTCOUNT(df['涨停'])
    # 统计涨停
    df['N天'], df['M板'] = limit_count(df['涨停'], 2)

    df['MA金叉'] = CROSS(df['sma_5'], df['sma_10'])

    # 内存优化
    df['收盘价10日排序'] = df['收盘价10日排序'].astype(np.float32)
    df['收盘价20日排序'] = df['收盘价20日排序'].astype(np.float32)
    df['连板'] = df['连板'].astype(np.uint16)
    df['N天'] = df['N天'].astype(np.int16)
    df['M板'] = df['M板'].astype(np.uint8)

    return df


def calc_cs(df: pd.DataFrame):
    """按date分组后，得到横截面每行，然后应用相应计算函数

    多少行调用多少次，一年就调用约250多次
    """
    # 先横截面分组
    df['close_rank'] = rank(df['close'])

    # 目前没有行情业数据，只能模拟行业分组
    df['industry'] = df['close_rank'] * 10 // 2

    return df


def calc_cs2(df: pd.DataFrame):
    """同行业的rank计算。按日期、行业进行分组再计算

    比横截面计算多N倍次数，N为行业数量
    """
    df['amount_rank'] = rank(df['amount'])
    return df
