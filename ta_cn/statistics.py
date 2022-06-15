import bottleneck as bn
import numpy as np

from .utils import np_to_pd


def AVEDEV(real, timeperiod: int = 5):
    """平均绝对偏差"""

    def mad(x):
        return np.abs(x - x.mean()).mean()

    return np_to_pd(real).rolling(window=timeperiod).apply(mad, raw=True)


def STD(real, timeperiod: int = 5):
    """样本标准差"""
    return bn.move_std(real, window=timeperiod, axis=0, ddof=1)


def STDP(real, timeperiod: int = 5):
    """总体标准差"""
    return bn.move_std(real, window=timeperiod, axis=0, ddof=0)


def VAR(real, timeperiod: int = 5):
    """样本方差"""
    return bn.move_var(real, window=timeperiod, axis=0, ddof=1)


def VARP(real, timeperiod: int = 5):
    """总体方差"""
    return bn.move_std(real, window=timeperiod, axis=0, ddof=0)
