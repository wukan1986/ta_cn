"""
K线相关计算
"""
# https://github.com/TA-Lib/ta-lib/blob/master/src/ta_func/ta_utility.h#L327
import numpy as np

from . import EPSILON
from .wq.time_series import ts_delay


# =========================================
# 单K线计算

def REALBODY(open_, high, low, close):
    """实体"""
    return (close - open_).abs()


def UPPERSHADOW(open_, high, low, close):
    """上影"""
    return high - np.maximum(open_, close)


def LOWERSHADOW(open_, high, low, close):
    """下影"""
    return np.minimum(open_, close) - low


def HIGHLOWRANGE(open_, high, low, close):
    """总长"""
    return high - low


def CANDLECOLOR(open_, high, low, close):
    """K线颜色"""
    return close >= open_


def UPPERBODY(open_, high, low, close):
    """实体上沿"""
    return np.maximum(open_, close)


def LOWERBODY(open_, high, low, close):
    """实体下沿"""
    return np.minimum(open_, close)


def efficiency_ratio_candle(open_, high, low, close):
    """K线内的市场效率。两个总长减去一个实体长就是路程

    比较粗略的计算市场效率的方法。丢失了部分路程信息，所以结果会偏大
    """
    displacement = REALBODY(open_, high, low, close)
    distance = 2 * HIGHLOWRANGE(open_, high, low, close) - displacement
    return displacement / (distance + EPSILON)


# =========================================
# 双K线计算

def REALBODYGAPUP(open_, high, low, close):
    """实体跳空高开。当天实体下界大于昨天实体上界"""
    upper = UPPERBODY(open_, high, low, close)
    lower = LOWERBODY(open_, high, low, close)
    return lower > ts_delay(upper, 1)


def REALBODYGAPDOWN(open_, high, low, close):
    """实体跳空低开。当天实体上界小于昨天实体下界"""
    upper = UPPERBODY(open_, high, low, close)
    lower = LOWERBODY(open_, high, low, close)
    return upper < ts_delay(lower, 1)


def CANDLEGAPUP(open_, high, low, close):
    """跳空高开。当天最低大于昨天最高"""
    return low > ts_delay(high, 1)


def CANDLEGAPDOWN(open_, high, low, close):
    """跳空低开。当天最高小于昨天最低"""
    return high < ts_delay(low, 1)
