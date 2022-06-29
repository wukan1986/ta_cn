"""

"""
import bottleneck as _bn
import numpy as _np


def signedpower(real, n):
    """保持符号的次方"""
    return _np.sign(real) * (abs(real) ** n)


def TS_RANK(real, timeperiod=10):
    """滚动rank"""
    t1 = _bn.move_rank(real, window=timeperiod, axis=0)
    return (t1 + 1.) / 2.


def RANK(real, pct=True):
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
