"""

"""
import numpy as _np

from . import bn_wraps as _bn


def signedpower(real, n):
    """保持符号的次方"""
    with _np.errstate(invalid='ignore', divide='ignore'):
        return _np.sign(real) * (abs(real) ** n)


def TS_RANK(real, timeperiod: int):
    """滚动rank

    real, timeperiod: int = 10
    """
    t1 = _bn.move_rank(real, window=timeperiod, axis=0)
    return (t1 + 1.) / 2.


def RANK(real):
    """横截面rank"""
    pct: bool = True

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


def scale(real, a):
    """横截面缩放

    scale(real, a=1)
    """
    if real.ndim == 2:
        b = _np.nansum(abs(real), axis=1, keepdims=True)
    else:
        b = _np.nansum(abs(real), keepdims=True)

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


def FILTER(A, condition):
    return _np.where(condition, A, 0)


def CUMPROD(A):
    if A.ndim == 2:
        return _np.cumprod(A, axis=0)
    else:
        return _np.cumprod(A)


def CUMSUM(A):
    if A.ndim == 2:
        return _np.cumsum(A, axis=0)
    else:
        return _np.cumsum(A)
