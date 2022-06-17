import talib as ta

from .logical import IF
from .maths import SGN
from .reference import SUM, DIFF, REF


def OBV(real, volume, scale=1):  # 能量潮指标
    """能量潮指标"""
    S = SGN(DIFF(real))
    # 第一天由0改成1就与talib一样了
    S[0] = 1
    return SUM(S * volume, 0)


def OBV_CN(real, volume, scale=1 / 10000):
    """能量潮指标中国版"""
    S = SGN(DIFF(real))
    # 同花顺最后会除10000，但东方财富没有除
    return SUM(S * volume, 0) * scale


def VR(close, volume, timeperiod=26):
    """VR容量比率"""
    LC = REF(close, timeperiod=1)
    return SUM(IF(close > LC, volume, 0), timeperiod) / SUM(IF(close <= LC, volume, 0), timeperiod) * 100
