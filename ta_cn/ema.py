import pandas as _pd

import ta_cn.talib as _ta2d
from ta_cn.talib import set_compatibility, TA_COMPATIBILITY_DEFAULT, TA_COMPATIBILITY_METASTOCK
from .ewm_nb import ewm_mean
from .nb import ma_1st, sum_1st
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


def EMA_0_TA(real, timeperiod=24):
    """EMA第一个值用MA"""
    set_compatibility(TA_COMPATIBILITY_DEFAULT)
    return _ta2d.EMA(real, timeperiod=timeperiod)


def EXPMEMA(real, timeperiod=24):
    """EMA第一个值用MA

    return np_to_pd(ma_1st(real, timeperiod)).ewm(span=timeperiod, min_periods=0, adjust=False).mean()
    """
    return ewm_mean(ma_1st(real, timeperiod), span=timeperiod, min_periods=0, adjust=False)


def EMA_1_TA(real, timeperiod=24):
    """EMA第一个值用Price"""
    set_compatibility(TA_COMPATIBILITY_METASTOCK)
    return _ta2d.EMA(real, timeperiod=timeperiod)


def EMA_1_PD(real, timeperiod=24):
    """EMA第一个值用Price

    return np_to_pd(real).ewm(span=timeperiod, min_periods=timeperiod, adjust=False).mean()
    """
    return ewm_mean(real, span=timeperiod, min_periods=timeperiod, adjust=False)


def SMA(real, timeperiod=24, M=1):
    """EMA第一个值用MA

    return np_to_pd(ma_1st(real, timeperiod)).ewm(alpha=M / timeperiod, min_periods=0, adjust=False).mean()
    """
    return ewm_mean(ma_1st(real, timeperiod), alpha=M / timeperiod, min_periods=0, adjust=False)


def DMA(real, alpha):
    """求X的动态移动平均。 0<alpha<1

    上一期值权重(1-alpha)，当前值权重alpha

    return np_to_pd(real).ewm(alpha=alpha, adjust=False).mean()
    """
    return ewm_mean(real, alpha=alpha, min_periods=0, adjust=False)


def WS_SUM(real: _pd.DataFrame, timeperiod: int = 5):
    """Wilder Smooth 威尔德平滑求和

    Notes
    -----
    在ADX/DMI这个指标中，数据的起始位置不是real，而是real的上层数据，所以需要将nan改成0

    """
    return np_to_pd(sum_1st(real, timeperiod)).ewm(alpha=1 / timeperiod, min_periods=timeperiod).sum()
