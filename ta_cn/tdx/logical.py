import numba
import numpy as np

from . import SUM
from .. import EPSILON
from ..nb import numpy_rolling_apply, _rolling_func_1_nb
from ..utils import np_to_pd, num_to_np, pd_to_np


def CROSS(S1, S2):
    """向上金叉"""
    # 可能输入单个数字，需预处理
    S1 = num_to_np(S1, S2)
    # 处理精度问题
    # 1. S1<=S2时，需要给S2范围大一点，表示等于
    # 2. S1>S2时，同样要给S2范围大一点，排除等于
    S2 = num_to_np(S2, S1) + EPSILON

    arr = np.zeros_like(S1, dtype=bool)
    # 输入为Series时对齐有差异，前面需转成numpy
    arr[1:] = (S1 <= S2)[:-1] & (S1 > S2)[1:]
    return arr


def EVERY(real, timeperiod):
    """最近timeperiod天是否全为True

    EVERY(real, timeperiod=5)
    """
    return SUM(real, timeperiod) == timeperiod


def EXIST(real, timeperiod):
    """最近timeperiod天是否存在一天为True

    EXIST(real, timeperiod=5)
    """
    return SUM(real, timeperiod) > 0


def BETWEEN(S, A, B):
    """BETWEEN(A,B,C)表示A处于B和C之间时返回1,否则返回0"""
    return ((A < S) & (S < B)) | ((A > S) & (S > B))


def VALUEWHEN(S, X):
    """条件跟随函数。当COND条件成立时,取X的当前值,否则取VALUEWHEN的上个值"""
    return np_to_pd(np.where(S, X, np.nan)).ffill()


@numba.jit(nopython=True, cache=True, nogil=True)
def _last_nb(arr, n, m):
    """LAST(X,A,B)，A>B，表示从前A日到前B日一致满足X条件"""
    return np.all(arr[:n - m])


def LAST(real, n, m):
    """LAST(X,A,B)，A>B，表示从前A日到前B日一致满足X条件

    LAST(real, n=20, m=10)
    """
    return numpy_rolling_apply([pd_to_np(real)], n, _rolling_func_1_nb, _last_nb, n, m)
