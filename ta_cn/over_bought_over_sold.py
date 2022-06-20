import talib as _ta1d
from talib import MA_Type

import ta_cn.talib as _ta2d
from .maths import MEAN
from .reference import LLV, HHV, REF, MA, TR
from .ta import TA_SET_COMPATIBILITY, TA_COMPATIBILITY_DEFAULT, TA_COMPATIBILITY_METASTOCK


def ATR_CN(high, low, close, timeperiod=14):
    """ATR真实波幅N日平均

    talib的ATR算法类似于EMA，所以要重写此处才与中国ATR相同
    """
    return MA(TR(high, low, close), timeperiod)


def BIAS(real, timeperiod=6):
    """BIAS乖离率

    Parameters
    ----------
    real
    timeperiod:int
        常用参数：6,12,24

    """
    return (real / MA(real, timeperiod) - 1) * 100


def KDJ(high, low, close, fastk_period=9, M1=3, M2=3):
    """KDJ指标

    talib中EMA的参数用法不同
    """
    TA_SET_COMPATIBILITY(TA_COMPATIBILITY_METASTOCK)

    K, D = _ta2d.STOCH(high, low, close,
                       fastk_period=fastk_period,
                       slowk_period=(M1 * 2 - 1), slowk_matype=MA_Type.EMA,
                       slowd_period=(M2 * 2 - 1), slowd_matype=MA_Type.EMA)

    J = K * 3 - D * 2
    return K, D, J


def ROC(real, timeperiod=12):  # 变动率指标
    """ROC变动率指标

    Parameters
    ----------
    real
    timeperiod:int
        常用参数：12

    Examples
    --------
    股票软件上常再求一次MA
    >>> MA(ROC(CLOSE, 12), 6)

    """
    if real.ndim == 2:
        return (real / REF(real, timeperiod) - 1) * 100
    else:
        return _ta1d.ROC(real, timeperiod=timeperiod)


def TYPPRICE(high, low, close):
    """典型价格。高低收的平均值"""
    if close.ndim == 2:
        return MEAN(high, low, close)
    else:
        return _ta1d.TYPPRICE(high, low, close)


def MEDPRICE(high, low):
    """中间价格。高低平均值"""
    if high.ndim == 2:
        return MEAN(high, low)
    else:
        return _ta1d.MEDPRICE(high, low)


def WR(high, low, close, timeperiod=10):
    """W&R威廉指标

    Parameters
    ----------
    high
    low
    close
    timeperiod: int
        常用参数：10, 6

    Returns
    -------

    """

    if close.ndim == 2:
        hh = HHV(high, timeperiod)
        ll = LLV(low, timeperiod)
        return (hh - close) / (hh - ll) * 100
    else:
        return _ta1d.WILLR(high, low, close, timeperiod=timeperiod)


def RSI(real, timeperiod=24):
    """RSI指标"""
    # 如果设置成1，将会多一个数字
    TA_SET_COMPATIBILITY(TA_COMPATIBILITY_DEFAULT)

    return _ta2d.RSI(real, timeperiod=timeperiod)
