"""这里存放因速度慢被淘汰的代码，因为有教学意义而保留"""
import numpy as _np
import pandas as _pd

from . import talib as ta
from .ema import EMA_1_PD, WS_SUM, SMA
from .maths import MAX, ABS
from .nb import fill_notna
from .over_bought_over_sold import ROC, TYPPRICE
from .reference import HHV, LLV, MA, REF, SUM, TR
from .statistics import AVEDEV
from .utils import np_to_pd

_ta1d = ta.init(mode=1, skipna=False)
_ta2d = ta.init(mode=2, skipna=False)


def ATR(high, low, close, timeperiod=14):
    """ATR真实波幅N日平均

    talib的ATR算法类似于SMA，所以要重写此处才与中国ATR相同
    """
    return SMA(TR(high, low, close), timeperiod)


def ATR_CN(high, low, close, timeperiod=14):
    """ATR真实波幅N日平均

    talib的ATR算法类似于EMA，所以要重写此处才与中国ATR相同
    """

    # 以下要慢一些，不采用了
    def func(high, low, close, timeperiod):
        return _ta1d.SMA(_ta1d.TRANGE(high, low, close), timeperiod)

    return _ta2d.tafunc_nditer_1(func, [high, low, close], {'timeperiod': timeperiod},
                                 ['high', 'low', 'close'], ['real'])


def MACD_CN(real: _pd.DataFrame, fastperiod=12, slowperiod=26, signalperiod=9):
    # 中国区使用公式自行实现的算法，由于多次用到EMA，效率不高，建议直接使用MACDEXT
    DIF = EMA_1_PD(real, fastperiod) - EMA_1_PD(real, slowperiod)
    DEA = EMA_1_PD(DIF, signalperiod)
    MACD = (DIF - DEA) * 2
    return DIF, DEA, MACD


def KDJ_CN(high, low, close, fastk_period=9, M1=3, M2=3):
    """KDJ指标"""
    hh = HHV(high, fastk_period)
    ll = LLV(low, fastk_period)
    RSV = (close - ll) / (hh - ll) * 100
    K = EMA_1_PD(RSV, (M1 * 2 - 1))
    D = EMA_1_PD(K, (M2 * 2 - 1))

    J = K * 3 - D * 2
    return K, D, J


def TRIX_CN(real, timeperiod=12):
    """三重指数平滑均线

    由EMA算法差异导致的不同
    """
    TR = EMA_1_PD(EMA_1_PD(EMA_1_PD(real, timeperiod), timeperiod), timeperiod)
    return ROC(TR, 1)


def CCI(high, low, close, timeperiod=14):
    """CCI顺势指标，talib版更快"""
    tp = TYPPRICE(high, low, close)
    return (tp - MA(tp, timeperiod)) / (0.015 * AVEDEV(tp, timeperiod))


def RSI(real, timeperiod=24):
    """RSI指标"""
    DIF = real - REF(real, 1)
    return SMA(MAX(DIF, 0), timeperiod, 1) / SMA(ABS(DIF), timeperiod, 1) * 100


def WMA(real, timeperiod=5):
    """加权移动平均"""

    def func(x):
        # 复制于MyTT,比tqsdk中tafunc中计算要快
        return x[::-1].cumsum().sum() * 2 / timeperiod / (timeperiod + 1)

    return np_to_pd(real).rolling(timeperiod).apply(func, raw=True)


def MFI(high, low, close, volume, timeperiod=14):
    """MFI指标"""
    tp = TYPPRICE(high, low, close)
    tpv = tp * volume
    # 比TALIB结果多一个数字，通过置空实现与TA-LIB完全一样
    tpv = fill_notna(tpv, fill_value=_np.nan, n=1)

    is_raising = tp > REF(tp, 1)
    pos_sum = SUM(is_raising * tpv, timeperiod)
    neg_sum = SUM(~is_raising * tpv, timeperiod)
    return 100 * pos_sum / (pos_sum + neg_sum)


def DM(high, low, timeperiod=14):
    """Directional Movement方向动量

    WS_SUM威尔德平滑求和
    """
    HD = high - REF(high, 1)
    LD = REF(low, 1) - low

    # REF导至出现空，处理一下，防止空值出现
    HD[_np.isnan(HD) & (~_np.isnan(high))] = 0
    LD[_np.isnan(LD) & (~_np.isnan(low))] = 0

    # talib中是用的威尔德平滑
    PDM = WS_SUM(((HD > 0) & (HD > LD)) * HD, timeperiod)
    MDM = WS_SUM(((LD > 0) & (LD > HD)) * LD, timeperiod)
    return PDM, MDM


def DM_CN(high, low, timeperiod=14):
    """中国版DM

    SUM滚动求和
    """
    HD = high - REF(high, 1)
    LD = REF(low, 1) - low
    # 而中国版一般是直接滚动求和
    PDM = SUM(((HD > 0) & (HD > LD)) * HD, timeperiod)
    MDM = SUM(((LD > 0) & (LD > HD)) * LD, timeperiod)
    return PDM, MDM


def DI(high, low, close, timeperiod=14):
    """Directional Indicator方向指标"""
    tr = TR(high, low, close)
    # 数据有效区开始，值由nan要设成0
    tr[_np.isnan(tr) & (~_np.isnan(close))] = 0

    TRS = WS_SUM(tr, timeperiod)
    # 比talib多一个，删除它
    TRS = fill_notna(TRS, fill_value=_np.nan, n=1)

    PDM, MDM = DM(high, low, timeperiod)
    PDI = PDM * 100 / TRS
    MDI = MDM * 100 / TRS
    return PDI, MDI


def DI_CN(high, low, close, timeperiod=14):
    """中国版DI

    区别是SUM与WS_SUM
    """
    TRS = SUM(TR(high, low, close), timeperiod)
    PDM, MDM = DM_CN(high, low, timeperiod)
    PDI = PDM * 100 / TRS
    MDI = MDM * 100 / TRS
    return PDI, MDI


def DMI(high, low, close, timeperiod=14):
    """趋向指标"""
    PDI, MDI = DI(high, low, close, timeperiod=timeperiod)
    ADX = SMA(ABS(PDI - MDI) / (PDI + MDI) * 100, timeperiod)
    # 这里timeperiod-1，才正好与talib对应
    ADXR = (ADX + REF(ADX, timeperiod - 1)) / 2
    return PDI, MDI, ADX, ADXR


def DMI_CN(high, low, close, timeperiod=14):
    # DI算法不同
    PDI, MDI = DI_CN(high, low, close, timeperiod=timeperiod)
    # ADX中的MA与SMA不同
    ADX = MA(ABS(PDI - MDI) / (PDI + MDI) * 100, timeperiod)
    # timeperiod与timeperiod-1不同
    ADXR = (ADX + REF(ADX, timeperiod)) / 2
    return PDI, MDI, ADX, ADXR


def _AVEDEV(real, timeperiod: int = 20):
    """平均绝对偏差,慢，请用nb版"""

    def mad(x):
        return _np.abs(x - x.mean()).mean()

    return np_to_pd(real).rolling(window=timeperiod).apply(mad, raw=True)


def _SLOPE(S, N=14):
    return np_to_pd(S).rolling(N).apply(lambda x: _np.polyfit(range(N), x, deg=1)[0], raw=True)


def _FORCAST(S, N=14):
    return np_to_pd(S).rolling(N).apply(lambda x: _np.polyval(_np.polyfit(range(N), x, deg=1), N - 1), raw=True)
