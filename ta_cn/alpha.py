"""

"""
import numpy as _np


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
