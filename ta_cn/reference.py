import bottleneck as bn
import numpy as np
import talib as ta

from .maths import MAX, ABS
from .utils import np_to_pd


def CONST(real):
    """取A最后的值为常量"""
    return np.full_like(real, real[-1])


def COUNT(real, timeperiod):
    """统计N周期中满足X条件的周期数"""
    return SUM(real, timeperiod)


def DIFF(real, timeperiod: int = 1):
    """差分"""
    return real - REF(real, timeperiod)


def HHV(real, timeperiod: int = 5):
    """求timeperiod周期内real最高值"""
    return bn.move_max(real, window=timeperiod, axis=0)


def HHVBARS(real, timeperiod: int = 5):
    """求timeperiod周期内real最高值到当前周期数"""
    return bn.move_argmax(real, window=timeperiod, axis=0)


def LLV(real, timeperiod: int = 5):
    """求timeperiod周期内real最低值"""
    return bn.move_min(real, window=timeperiod, axis=0)


def LLVBARS(real, timeperiod: int = 5):
    """求timeperiod周期内real最低值到当前周期数"""
    return bn.move_argmin(real, window=timeperiod, axis=0)


def REF(real, timeperiod: int = 1):
    """向前引用"""
    arr = np.full(real.shape, np.nan)
    arr[timeperiod:] = real[:-timeperiod]
    return arr


def SUM(real, timeperiod: int = 5):
    """时序滚动求和

    Parameters
    ----------
    real
    timeperiod: int
        滚动周期
        0表示全量即累计求和

    """
    if timeperiod > 0:
        return bn.move_sum(real, window=timeperiod, axis=0)
    else:
        # 0表示全量累计求和
        return np.nancumsum(real, axis=0)


def TR(high, low, close):
    """TR真实波幅"""
    if close.ndim == 2:
        lc = REF(close, 1)
        return MAX(high - low, ABS(high - lc), ABS(lc - low))
    else:
        return ta.TRANGE(high, low, close)


def MA(real, timeperiod: int = 5):
    """简单移动平均

    等价于talib中的SMA"""
    return bn.move_mean(real, window=timeperiod, axis=0)


def WMA(real, timeperiod=5):
    """加权移动平均"""
    if real.ndim == 2:
        def func(x):
            # 复制于MyTT,比tqsdk中tafunc中计算要快
            return x[::-1].cumsum().sum() * 2 / timeperiod / (timeperiod + 1)

        return np_to_pd(real).rolling(timeperiod).apply(func, raw=True)
    else:
        return ta.WMA(real, timeperiod=timeperiod)
