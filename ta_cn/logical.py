import numpy as np

from .nb import _FILTER_1d_nb, _FILTER_2d_nb
from .reference import SUM
from .utils import pd_to_np, np_to_pd


def CROSS(S1, S2):
    """向上金叉"""
    arr = np.full_like(S1, fill_value=False, dtype=bool)
    arr[1:] = (S1 <= S2)[:-1] & (S1 > S2)[1:]
    return arr


def IF(condition, T, F):
    """序列布尔判断"""
    return np.where(condition, T, F)


def EVERY(real, timeperiod=5):
    """最近timeperiod天是否全为True"""
    return SUM(real, timeperiod) == timeperiod


def EXIST(real, timeperiod=5):
    """最近timeperiod天是否存在一天为True"""
    return SUM(real, timeperiod) > 0


def FILTER(S, N):
    """FILTER函数，S满足条件后，将其后N周期内的数据置为0"""
    S = pd_to_np(S, copy=True)
    if S.ndim == 2:
        _FILTER_2d_nb(S, N)
    else:
        _FILTER_1d_nb(S, N)
    return S


def BETWEEN(S, A, B):
    """BETWEEN(A,B,C)表示A处于B和C之间时返回1,否则返回0"""
    return ((A < S) & (S < B)) | ((A > S) & (S > B))


def VALUEWHEN(S, X):
    """"""
    return np_to_pd(np.where(S, X, np.nan)).ffill()
