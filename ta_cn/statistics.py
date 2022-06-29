import bottleneck as _bn
import numpy as _np

import ta_cn.talib as _ta2d
from .nb import numpy_rolling_apply, _rolling_func_1_nb, _avedev_nb, _slope_nb, _rolling_func_2_nb, _cov_nb
from .utils import pd_to_np


def AVEDEV(real, timeperiod=20):
    """平均绝对偏差"""
    return numpy_rolling_apply([pd_to_np(real)], timeperiod, _rolling_func_1_nb, _avedev_nb)


def SLOPE(real, timeperiod=14):
    """线性回归斜率

    Parameters
    ----------
    real
    timeperiod

    References
    ----------
    https://github.com/TA-Lib/ta-lib/blob/master/src/ta_func/ta_LINEARREG_SLOPE.c

    """
    return _ta2d.LINEARREG_SLOPE(real, timeperiod=timeperiod)
    # !!! 以下代码也很有价值，不要删除
    x = _np.arange(timeperiod)
    m_x = _np.mean(x)
    return numpy_rolling_apply([pd_to_np(real)], timeperiod, _rolling_func_1_nb, _slope_nb, x, m_x)


def FORCAST(real, timeperiod=14):
    """线性回归预测值

    Parameters
    ----------
    real
    timeperiod

    References
    ----------
    https://github.com/TA-Lib/ta-lib/blob/master/src/ta_func/ta_LINEARREG.c

    """
    return _ta2d.LINEARREG(real, timeperiod=timeperiod)


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


def CORREL(real0, real1, timeperiod=30):
    """滚动相关系数"""
    return _ta2d.CORREL(real0, real1, timeperiod=timeperiod)


def COVAR(real0, real1, timeperiod=30):
    """滚动协方差"""
    return numpy_rolling_apply([pd_to_np(real0), pd_to_np(real1)],
                               timeperiod, _rolling_func_2_nb, _cov_nb)
