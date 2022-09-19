"""

"""
import numpy as np


def FILTER_191(A, condition):
    """注意：与TDX中的FILTER不同"""
    return np.where(condition, A, 0)


def CUMPROD(A):
    return np.cumprod(A, axis=0)


def CUMSUM(A):
    return np.cumsum(A, axis=0)
