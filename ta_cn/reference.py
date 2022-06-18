import bottleneck as _bn
import numpy as _np

from .maths import MAX, ABS


def CONST(real):
    """取A最后的值为常量"""
    return _np.full_like(real, real[-1])


def COUNT(real, timeperiod):
    """统计N周期中满足X条件的周期数"""
    return SUM(real, timeperiod)


def DIFF(real, timeperiod: int = 1):
    """差分"""
    return real - REF(real, timeperiod)


def HHV(real, timeperiod: int = 5):
    """求timeperiod周期内real最高值"""
    return _bn.move_max(real, window=timeperiod, axis=0)


def HHVBARS(real, timeperiod: int = 5):
    """求timeperiod周期内real最高值到当前周期数"""
    return _bn.move_argmax(real, window=timeperiod, axis=0)


def LLV(real, timeperiod: int = 5):
    """求timeperiod周期内real最低值"""
    return _bn.move_min(real, window=timeperiod, axis=0)


def LLVBARS(real, timeperiod: int = 5):
    """求timeperiod周期内real最低值到当前周期数"""
    return _bn.move_argmin(real, window=timeperiod, axis=0)


def REF(real, timeperiod: int = 1):
    """向前引用，特意模仿shift"""
    if timeperiod == 0:
        # 该不该复制呢？
        return real  # .copy()
    if timeperiod > 0:
        arr = _np.full(real.shape, _np.nan)
        arr[timeperiod:] = real[:-timeperiod]
    if timeperiod < 0:
        arr = _np.full(real.shape, _np.nan)
        arr[:timeperiod] = real[-timeperiod:]
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
        return _bn.move_sum(real, window=timeperiod, axis=0)
    else:
        # 0表示全量累计求和
        return _np.cumsum(real, axis=0)


def TR(high, low, close):
    """TR真实波幅"""
    lc = REF(close, 1)
    return MAX(high - low, ABS(high - lc), ABS(lc - low))


def MA(real, timeperiod: int = 5):
    """简单移动平均

    等价于talib中的SMA"""
    return _bn.move_mean(real, window=timeperiod, axis=0)
