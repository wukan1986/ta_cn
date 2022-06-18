import bottleneck as _bn
import numpy as _np

from .nb import numpy_rolling_apply, _rolling_func_nb, _avedev_nb, _slope_nb
from .utils import pd_to_np


def AVEDEV(real, timeperiod=20):
    """平均绝对偏差"""
    return numpy_rolling_apply(pd_to_np(real), timeperiod, _rolling_func_nb, _avedev_nb)


def SLOPE(real, timeperiod=14):
    """线性回归斜率"""
    x = _np.arange(timeperiod)
    m_x = _np.mean(x)
    return numpy_rolling_apply(pd_to_np(real), timeperiod, _rolling_func_nb, _slope_nb, x, m_x)


def STD(real, timeperiod: int = 5):
    """样本标准差"""
    return _bn.move_std(real, window=timeperiod, axis=0, ddof=1)


def STDP(real, timeperiod: int = 5):
    """总体标准差"""
    return _bn.move_std(real, window=timeperiod, axis=0, ddof=0)


def VAR(real, timeperiod: int = 5):
    """样本方差"""
    return _bn.move_var(real, window=timeperiod, axis=0, ddof=1)


def VARP(real, timeperiod: int = 5):
    """总体方差"""
    return _bn.move_std(real, window=timeperiod, axis=0, ddof=0)
