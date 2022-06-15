import numpy as np
import talib as ta

from .logical import IF
from .maths import SGN
from .nb import fill_notna
from .over_bought_over_sold import TYP
from .reference import SUM, DIFF, REF


def OBV(real, volume, scale=1):  # 能量潮指标
    """能量潮指标"""
    if real.ndim == 2:
        S = SGN(DIFF(real))
        # 第一天由0改成1就与talib一样了
        S[0] = 1
        return SUM(S * volume, 0)
    else:
        # talib中第一天的成交量正数，但中国区当成0
        return ta.OBV(real, volume)


def OBV_CN(real, volume, scale=1 / 10000):
    """能量潮指标中国版"""
    S = SGN(DIFF(real))
    # 同花顺最后会除10000，但东方财富没有除
    return SUM(S * volume, 0) * scale


def VR(close, volume, timeperiod=26):
    """VR容量比率"""
    LC = REF(close, timeperiod=1)
    return SUM(IF(close > LC, volume, 0), timeperiod) / SUM(IF(close <= LC, volume, 0), timeperiod) * 100


def MFI(high, low, close, volume, timeperiod=14):
    """MFI指标"""
    tp = TYP(high, low, close)
    tpv = tp * volume
    # 比TALIB结果多一个数字，通过置空实现与TA-LIB完全一样
    tpv = fill_notna(tpv, fill_value=np.nan, n=1)

    is_raising = tp > REF(tp, 1)
    pos_sum = SUM(is_raising * tpv, timeperiod)
    neg_sum = SUM(~is_raising * tpv, timeperiod)
    return 100 * pos_sum / (pos_sum + neg_sum)
