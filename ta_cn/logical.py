import numpy as _np

from .nb import _filter
from .reference import SUM
from .utils import np_to_pd

FILTER = _filter


def CROSS(S1, S2):
    """向上金叉"""
    arr = _np.full_like(S1, fill_value=False, dtype=bool)
    arr[1:] = (S1 <= S2)[:-1] & (S1 > S2)[1:]
    return arr


def IF(condition, T, F):
    """序列布尔判断"""
    return _np.where(condition, T, F)


def EVERY(real, timeperiod=5):
    """最近timeperiod天是否全为True"""
    return SUM(real, timeperiod) == timeperiod


def EXIST(real, timeperiod=5):
    """最近timeperiod天是否存在一天为True"""
    return SUM(real, timeperiod) > 0


def BETWEEN(S, A, B):
    """BETWEEN(A,B,C)表示A处于B和C之间时返回1,否则返回0"""
    return ((A < S) & (S < B)) | ((A > S) & (S > B))


def VALUEWHEN(S, X):
    """"""
    return np_to_pd(_np.where(S, X, _np.nan)).ffill()
