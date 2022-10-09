import numba
import numpy as np

from . import ABS, MAX, REF
from .. import bn_wraps as bn, numba_cache
from .. import talib as ta
from ..nb import numpy_rolling_apply, _rolling_func_1_nb
from ..utils import pd_to_np

_ta1d = ta.init(mode=1, skipna=False, to_globals=False)
_ta2d = ta.init(mode=2, skipna=False, to_globals=False)


def CONST(real):
    """取A最后的值为常量"""
    return np.full_like(real, real[-1])


def SUMIF(real, condition, timeperiod):
    """!!!注意，condition位置"""
    return bn.move_sum(real * condition, window=timeperiod, axis=0)


def TR(high, low, close):
    """TR真实波幅"""
    lc = REF(close, 1)
    return MAX(high - low, ABS(high - lc), ABS(lc - low))


def FILTER(S, N):
    """FILTER函数，S满足条件后，将其后N周期内的数据置为0"""

    @numba.jit(nopython=True, cache=numba_cache, nogil=True)
    def _filter_nb(arr, n):
        is_1d = arr.ndim == 1
        x = arr.shape[0]
        y = 1 if is_1d else arr.shape[1]

        for j in range(y):
            a = arr if is_1d else arr[:, j]

            # 为了跳过不必要部分，由for改while
            i = 0
            while i < x:
                if a[i]:
                    a[i + 1:i + 1 + n] = 0
                    i += n + 1
                else:
                    i += 1
        return arr

    S = pd_to_np(S, copy=True)
    return _filter_nb(S, N)


def BARSLAST(S):
    """BARSLAST(X)，上一次X不为0到现在的天数

    成立当天输出0
    """

    @numba.jit(nopython=True, cache=True, nogil=True)
    def _bars_last_nb(arr, out):
        """上一次条件成立到当前的周期数"""
        is_1d = arr.ndim == 1
        x = arr.shape[0]
        y = 1 if is_1d else arr.shape[1]

        for j in range(y):
            a = arr if is_1d else arr[:, j]
            b = out if is_1d else out[:, j]
            s = 0
            for i in range(x):
                if a[i]:
                    s = 0
                b[i] = s
                s += 1

        return out

    S = pd_to_np(S, copy=False)
    out = np.zeros_like(S, dtype=int)
    return _bars_last_nb(S, out)


def BARSLASTCOUNT(S):
    """BARSLASTCOUNT(X)，统计连续满足X条件的周期数

    成立第一天输出1
    """

    @numba.jit(nopython=True, cache=numba_cache, nogil=True)
    def _bars_last_count_nb(arr, out):
        """

        Parameters
        ----------
        arr
        out

        References
        ----------
        https://stackoverflow.com/questions/18196811/cumsum-reset-at-nan

        """
        is_1d = arr.ndim == 1
        x = arr.shape[0]
        y = 1 if is_1d else arr.shape[1]

        for j in range(y):
            a = arr if is_1d else arr[:, j]
            b = out if is_1d else out[:, j]
            s = 0
            for i in range(x):
                if a[i]:
                    s += 1
                    b[i] = s
                else:
                    s = 0

        return out

    S = pd_to_np(S, copy=False)
    out = np.zeros_like(S, dtype=int)
    return _bars_last_count_nb(S, out)


def BARSSINCEN(cond, timeperiod):
    """BARSSINCEN(X,N):N周期内第一次X不为0到现在的天数"""

    @numba.jit(nopython=True, cache=numba_cache, nogil=True)
    def _bars_since_n_nb(a, n):
        """BARSSINCEN(X,N):N周期内第一次X不为0到现在的天数"""
        for i, x in enumerate(a):
            if x:
                return n - i - 1
        return 0

    return numpy_rolling_apply([pd_to_np(cond)], timeperiod, _rolling_func_1_nb, _bars_since_n_nb, timeperiod)


def FINDHIGH(var, n, m, t):
    """var在N日前的M天内第T个最高价"""
    t = var[-n-m:-n]
    t = np.unique(t)
    return t[-t]


def FINDHIGHBARS(var, n, m, t):
    """var在N日前的M天内第T个最高价到当前周期的周期数"""
    temp = var[-n-m:-n]
    temp = np.unique(temp)
    value = temp[-t]
    index = len(var)-np.where(var == value)[0][0]
    return index


def FINDLOW(var, n, m, t):
    """寻找指定周期内的特定最小值"""
    t = var[-n-m:-n]
    t = np.unique(t)
    return t[t]


def FINDLOWBARS(var, n, m, t):
    """寻找指定周期内的特定最小值到当前周期的周期数"""
    temp = var[-n-m:-n]
    temp = np.unique(temp)
    value = temp[t]
    index = len(var)-np.where(var == value)[0][0]
    return index
