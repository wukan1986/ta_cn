import numba
import numpy as np

from ta_cn import talib as ta, bn_wraps as bn
from ta_cn.nb import numpy_rolling_apply, _rolling_func_1_nb
from ta_cn.utils import pd_to_np

_ta1d = ta.init(mode=1, skipna=False)
_ta2d = ta.init(mode=2, skipna=False)


def AVEDEV(real, timeperiod: int):
    """平均绝对偏差

    AVEDEV(real, timeperiod=20)
    """

    @numba.jit(nopython=True, cache=True, nogil=True)
    def _avedev_nb(a):
        """avedev平均绝对偏差"""
        return np.mean(np.abs(a - np.mean(a)))

    return numpy_rolling_apply([pd_to_np(real)], timeperiod, _rolling_func_1_nb, _avedev_nb)


def STD(x, d):
    """样本标准差"""
    return bn.move_std(x, window=d, axis=0, ddof=1)


def STDP(x, d):
    """总体标准差"""
    return bn.move_std(x, window=d, axis=0, ddof=0)


def VAR(x, d):
    """样本方差"""
    return bn.move_var(x, window=d, axis=0, ddof=1)


def VARP(x, d):
    """总体方差"""
    return bn.move_var(x, window=d, axis=0, ddof=0)