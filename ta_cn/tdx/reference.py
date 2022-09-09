import numba
import numpy as np

from ta_cn import bn_wraps as bn
from ta_cn import talib as ta
from ta_cn.nb import _filter_nb, _bars_last_nb, _bars_last_count_nb, numpy_rolling_apply, _rolling_func_1_nb
from ta_cn.utils import pd_to_np
from ta_cn.wq.arithmetic import abs_ as ABS
from ta_cn.wq.arithmetic import max_ as MAX
from ta_cn.wq.time_series import ts_delay as REF

_ta1d = ta.init(mode=1, skipna=False)
_ta2d = ta.init(mode=2, skipna=False)


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
    S = pd_to_np(S, copy=True)
    return _filter_nb(S, N)


def BARSLAST(S):
    """BARSLAST(X)，上一次X不为0到现在的天数

    成立当天输出0
    """
    S = pd_to_np(S, copy=False)
    out = np.zeros_like(S, dtype=int)
    return _bars_last_nb(S, out)


def BARSLASTCOUNT(S):
    """BARSLASTCOUNT(X)，统计连续满足X条件的周期数

    成立第一天输出1
    """
    S = pd_to_np(S, copy=False)
    out = np.zeros_like(S, dtype=int)
    return _bars_last_count_nb(S, out)


def BARSSINCEN(cond, timeperiod):
    """BARSSINCEN(X,N):N周期内第一次X不为0到现在的天数"""

    @numba.jit(nopython=True, cache=True, nogil=True)
    def _bars_since_n_nb(a, n):
        """BARSSINCEN(X,N):N周期内第一次X不为0到现在的天数"""
        for i, x in enumerate(a):
            if x:
                return n - i - 1
        return 0

    return numpy_rolling_apply([pd_to_np(cond)], timeperiod, _rolling_func_1_nb, _bars_since_n_nb, timeperiod)
