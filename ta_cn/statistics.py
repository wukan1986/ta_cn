from . import bn_wraps as _bn
from . import talib as ta
from .nb import numpy_rolling_apply, _rolling_func_1_nb, _avedev_nb, _rolling_func_2_nb, _cov_nb
from .utils import pd_to_np

_ta1d = ta.init(mode=1, skipna=False)
_ta2d = ta.init(mode=2, skipna=False)


def AVEDEV(real, timeperiod: int):
    """平均绝对偏差

    AVEDEV(real, timeperiod=20)
    """
    return numpy_rolling_apply([pd_to_np(real)], timeperiod, _rolling_func_1_nb, _avedev_nb)


def STD(real, timeperiod: int):
    """样本标准差

    STD(real, timeperiod: int = 5)
    """
    return _bn.move_std(real, window=timeperiod, axis=0, ddof=1)


def STDP(real, timeperiod: int):
    """总体标准差

    STDP(real, timeperiod: int = 5)
    """
    # TODO: 这里有问题
    # if real.ndim == 2:
    #     return _bn.move_std(real, window=timeperiod, axis=0, ddof=0)
    # else:
    #     return _ta1d.STDDEV(real, timeperiod=timeperiod)

    if real.ndim == 2:
        return _ta2d.STDDEV(real, timeperiod=timeperiod)
    else:
        return _ta1d.STDDEV(real, timeperiod=timeperiod)

    # return _bn.move_std(real, window=timeperiod, axis=0, ddof=0)
    # if real.ndim == 2:
    #     return _ta2d.STDDEV(real, timeperiod=timeperiod)
    #     return _bn.move_std(real, window=timeperiod, axis=0, ddof=0)
    # else:
    #     return _ta1d.STDDEV(real, timeperiod=timeperiod)


def VAR(real, timeperiod: int):
    """样本方差

    VAR(real, timeperiod: int = 5)
    """
    return _bn.move_var(real, window=timeperiod, axis=0, ddof=1)


def VARP(real, timeperiod: int):
    """总体方差

    VARP(real, timeperiod: int = 5)
    """
    return _bn.move_var(real, window=timeperiod, axis=0, ddof=0)


def CORREL(real0, real1, timeperiod):
    """滚动相关系数

    CORREL(real0, real1, timeperiod=30)
    """
    return _ta2d.CORREL(real0, real1, timeperiod=timeperiod)


def COVAR(real0, real1, timeperiod):
    """滚动协方差

    COVAR(real0, real1, timeperiod=30)
    """
    return numpy_rolling_apply([pd_to_np(real0), pd_to_np(real1)],
                               timeperiod, _rolling_func_2_nb, _cov_nb)
