import talib as ta
from talib import MA_Type

from .ema import EMA_1_PD, SMA
from .maths import MEAN, MAX, ABS
from .reference import LLV, HHV, TR, REF, MA
from .statistics import AVEDEV


def ATR(high, low, close, timeperiod=20):
    """ATR真实波幅N日平均"""
    if close.ndim == 2:
        return MA(TR(high, low, close), timeperiod)
    else:
        # talib的ATR算法类似于EMA，所以要重写此处才与中国ATR相同
        return ta.SMA(ta.TRANGE(high, low, close), timeperiod=timeperiod)


def BIAS(real, timeperiod=6):
    """BIAS乖离率

    Parameters
    ----------
    real
    timeperiod:int
        常用参数：6,12,24

    """
    return (real / MA(real, timeperiod) - 1) * 100


def CCI(high, low, close, timeperiod=14):
    if close.ndim == 2:
        tp = TYP(high, low, close)
        return (tp - MA(tp, timeperiod)) / (0.015 * AVEDEV(tp, timeperiod))
    else:
        # AVEDEV计算慢，talib要快一些
        return ta.CCI(high, low, close, timeperiod=timeperiod)


def KDJ(close, high, low, fastk_period=9, M1=3, M2=3):
    """KDJ指标"""
    if close.ndim == 2:
        hh = HHV(high, fastk_period)
        ll = LLV(low, fastk_period)
        RSV = (close - ll) / (hh - ll) * 100
        K = EMA_1_PD(RSV, (M1 * 2 - 1))
        D = EMA_1_PD(K, (M2 * 2 - 1))
    else:
        # talib中EMA的参数用法不同
        K, D = ta.STOCH(high, low, close,
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
        return ta.ROC(real, timeperiod=timeperiod)


def TYP(high, low, close):
    """典型价格。高低收的平均值"""
    if close.ndim == 2:
        return MEAN(high, low, close)
    else:
        return ta.TYPPRICE(high, low, close)


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
        return ta.WILLR(high, low, close, timeperiod=timeperiod)


def RSI(real, timeperiod=24):
    """RSI指标"""
    if real.ndim == 2:
        DIF = real - REF(real, 1)
        return SMA(MAX(DIF, 0), timeperiod, 1) / SMA(ABS(DIF), timeperiod, 1) * 100
    else:
        # 请在循环外调用
        ta.set_compatibility(0)
        # 如果设置成1，将会多一个数字
        return ta.RSI(real, timeperiod=timeperiod)
