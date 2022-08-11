"""

"""
from .bn_wraps import _bn
import numpy as _np


def signedpower(real, n):
    """保持符号的次方"""
    return _np.sign(real) * (abs(real) ** n)


def TS_RANK(real, timeperiod: int = 10):
    """滚动rank"""
    t1 = _bn.move_rank(real, window=timeperiod, axis=0)
    return (t1 + 1.) / 2.


def RANK(real, pct: bool = True):
    """横截面rank"""
    if real.ndim == 2:
        t1 = _bn.nanrankdata(real, axis=1)
        t2 = _np.nansum(~_np.isnan(real), axis=1, keepdims=True)
    else:
        t1 = _bn.nanrankdata(real)
        t2 = _np.nansum(~_np.isnan(real))
    if pct:
        return t1 / t2
    else:
        return t1


def scale(real, a=1):
    """横截面缩放"""
    if real.ndim == 2:
        b = _np.nansum(abs(real), axis=1, keepdims=True)
    else:
        b = _np.nansum(abs(real))

    return real / b * a


def LessThan(x, y):
    # ValueError: Can only compare identically-labeled Series objects
    return x - y < 0


def split_adjust(real):
    """将后复权因子转成前复权"""
    if isinstance(real, _np.ndarray):
        return real / real[-1]
    else:
        return real / real.iloc[-1]
