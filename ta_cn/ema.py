import numpy as np
import pandas as pd

import ta_cn.talib as ta2d
from .ta import TA_SET_COMPATIBILITY, TA_COMPATIBILITY_DEFAULT, TA_COMPATIBILITY_METASTOCK
from .utils import np_to_pd

"""
由于MA有太多种了，单独提到此处，方便对比

默认EMA算法中，上一期值权重(timeperiod-1)/(timeperiod+1)，当前值权重2/(timeperiod+1)
ta.set_compatibility建议放在循环前执行

References
----------
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html?highlight=ewm#pandas.DataFrame.ewm
https://stackoverflow.com/questions/42869495/numpy-version-of-exponential-weighted-moving-average-equivalent-to-pandas-ewm

Warnings
--------
由于EMA的计算特点，只要调用了此文件中的公式，都需要预留一些数据，数据太短可能导致起点不同值不同

"""


def _MA_EMA(real, timeperiod, com=None, span=None, alpha=None):
    """内部函数。先计算MA做第一个值，然后再算EMA

    好几处开头的MA算法是一样的，但EMA的参数不同

    Notes
    -----
    二维矩阵如果开头有NaN，那么求均值的位置就不统一，得做特别处理

    """
    real = np_to_pd(real, copy=True)  # 开头部分将写入SMA
    ma = np_to_pd(np.zeros_like(real), copy=False)  # 来计算sma

    # 取最长位置, 用于计算SMA，没有必要全算一次MA
    max_end = real.notna().idxmax() + timeperiod
    if hasattr(max_end, 'max'):
        max_end = max_end.max()

    # 计算ma
    ma[:max_end] = real[:max_end].rolling(window=timeperiod, min_periods=timeperiod).mean()
    # 计算需要复制的区域,此区前部分为NaN,最后为mean
    mask = ma.isna().shift(fill_value=True)
    real[mask] = ma
    return real.ewm(com=com, span=span, alpha=alpha, min_periods=0, adjust=False).mean()


def EMA_0_TA(real, timeperiod=24):
    """EMA第一个值用MA"""
    TA_SET_COMPATIBILITY(TA_COMPATIBILITY_DEFAULT)
    return ta2d.EMA(real, timeperiod=timeperiod)


def EMA_0_PD(real, timeperiod=24):
    """EMA第一个值用MA"""
    return _MA_EMA(real, timeperiod=timeperiod, span=timeperiod)


def EMA_1_TA(real, timeperiod=24):
    """EMA第一个值用Price"""
    TA_SET_COMPATIBILITY(TA_COMPATIBILITY_METASTOCK)
    return ta2d.EMA(real, timeperiod=timeperiod)


def EMA_1_PD(real, timeperiod=24):
    """EMA第一个值用Price

    不少用到此指标，导致的计算过慢，如果原talib中有对应指标，并且与国内差别不大的情况下，可以迭代talib使用
    """
    return np_to_pd(real).ewm(span=timeperiod, min_periods=timeperiod, adjust=False).mean()


def SMA(real, timeperiod=24, M=1):
    """EMA第一个值用MA"""
    return _MA_EMA(real, timeperiod=timeperiod, alpha=M / timeperiod)


def DMA(real, alpha):
    """求X的动态移动平均。 0<alpha<1

    上一期值权重(1-alpha)，当前值权重alpha
    """
    return np_to_pd(real).ewm(alpha=alpha, adjust=False).mean()


def WS_SUM(real: pd.DataFrame, timeperiod: int = 5):
    """Wilder Smooth 威尔德平滑求和"""
    # 二维数据起始位置不同时，这里的算法会有问题
    # TODO: 还要再检查
    real = np_to_pd(real, copy=True)
    real[timeperiod - 1:timeperiod] = np.nansum(real[:timeperiod], axis=0)
    real[:timeperiod - 1] = 0

    return real.ewm(alpha=1 / timeperiod, min_periods=timeperiod).sum()

# if __name__ == '__main__':
#     import matplotlib.pyplot as plt
#
#     b = np.random.rand(10000).reshape(-1, 2)
#     b[:30, 0] = np.nan
#     b[:35, 1] = np.nan
#     a = b[:, 0]
#
#     r3 = WS_SUM(b).loc[:, 0]
#
#     r2 = EMA_0_PD(b).loc[:, 0]
#     r1 = EMA_0_TA(a)
#     pd.DataFrame({'DEFAULT_TALIB': r1, 'DEFAULT_PANDAS': r2}).plot()
#     pd.DataFrame({'DEFAULT_PANDAS': r2, 'DEFAULT_TALIB': r1}).plot()
#     plt.show()
#
#     r1 = EMA_1_TA(a)
#     r2 = EMA_1_PD(a)
#     pd.DataFrame({'METASTOCK_TALIB': r1, 'METASTOCK_PANDAS': r2}).plot()
#     pd.DataFrame({'METASTOCK_PANDAS': r2, 'METASTOCK_TALIB': r1}).plot()
#     plt.show()
