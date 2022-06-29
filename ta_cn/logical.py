import numpy as _np

from .nb import numpy_rolling_apply, _rolling_func_1_nb, _last_nb
from .reference import SUM
from .utils import np_to_pd, num_to_np, pd_to_np


def CROSS(S1, S2):
    """向上金叉"""
    # 可能输入单个数字，需预处理
    S1 = num_to_np(S1, S2)
    S2 = num_to_np(S2, S1)

    arr = _np.zeros_like(S1, dtype=bool)
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
    """条件跟随函数。当COND条件成立时,取X的当前值,否则取VALUEWHEN的上个值"""
    return np_to_pd(_np.where(S, X, _np.nan)).ffill()


def LAST(real, n=20, m=10):
    """LAST(X,A,B)，A>B，表示从前A日到前B日一致满足X条件"""
    return numpy_rolling_apply([pd_to_np(real)], n, _rolling_func_1_nb, _last_nb, n, m)
