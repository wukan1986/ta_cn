"""

"""
import numpy as np


def split_adjust(real):
    """将后复权因子转成前复权"""
    if isinstance(real, np.ndarray):
        return real / real[-1]
    else:
        return real / real.iloc[-1]


def FILTER(A, condition):
    return np.where(condition, A, 0)


def CUMPROD(A):
    if A.ndim == 2:
        return np.cumprod(A, axis=0)
    else:
        return np.cumprod(A)


def CUMSUM(A):
    if A.ndim == 2:
        return np.cumsum(A, axis=0)
    else:
        return np.cumsum(A)
