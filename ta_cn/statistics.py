import bottleneck as _bn

from .nb import _avedev

"""平均绝对偏差"""
AVEDEV = _avedev


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
