from .logical import IF
from .maths import SGN
from .reference import SUM, DIFF, REF


def OBV(real, volume, scale):  # 能量潮指标
    """能量潮指标

    OBV(real, volume, scale=1)
    """
    # 同花顺最后会除10000，但东方财富没有除 scale=1 / 10000
    return SUM(SGN(DIFF(real)) * volume, 0) * scale


def VR(close, volume, timeperiod: int):
    """VR容量比率

    VR(close, volume, timeperiod=26)
    """
    LC = REF(close, timeperiod=1)
    return SUM(IF(close > LC, volume, 0), timeperiod) / SUM(IF(close <= LC, volume, 0), timeperiod) * 100
