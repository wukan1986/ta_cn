import numpy as np
import pandas as pd
import talib as ta
from talib import MA_Type

from .ema import WS_SUM, EMA_1_PD, SMA
from .maths import MEAN, ABS
from .nb import fill_notna
from .over_bought_over_sold import ROC
from .reference import COUNT, REF, DIFF, TR, SUM, MA


def BBI(real, timeperiod1=3, timeperiod2=6, timeperiod3=12, timeperiod4=24):
    """BBI多空指标"""
    return MEAN(MA(real, timeperiod1),
                MA(real, timeperiod2),
                MA(real, timeperiod3),
                MA(real, timeperiod4))


def DPO(real, timeperiod=20):
    """DPO区间震荡线

    Parameters
    ----------
    real
    timeperiod:int
        常用参数：12

    Examples
    --------
    股票软件上常再求一次MA
    >>> MA(DPO(CLOSE, 20), 6)

    """
    return real - REF(MA(real, timeperiod), timeperiod // 2)


def MACD(real: pd.DataFrame, fastperiod=12, slowperiod=26, signalperiod=9):
    """MACD指标"""
    if real.ndim == 2:
        DIF = EMA_1_PD(real, fastperiod) - EMA_1_PD(real, slowperiod)
        DEA = EMA_1_PD(DIF, signalperiod)
        MACD = (DIF - DEA) * 2
        return DIF, DEA, MACD
    else:
        macd, macdsignal, macdhist = ta.MACDEXT(real,
                                                fastperiod=fastperiod, fastmatype=MA_Type.EMA,
                                                slowperiod=slowperiod, slowmatype=MA_Type.EMA,
                                                signalperiod=signalperiod, signalmatype=MA_Type.EMA)
        # macd起始位不是按slowperiod-1，而是按slowperiod+signalperiod-2，可能是为了三个输出的起始位相同
        # talib中的MACD没有*2
        return macd, macdsignal, macdhist * 2


def MTM(real, timeperiod=12):  # 动量指标
    """MTM动量指标

    Parameters
    ----------
    real
    timeperiod:int
        常用参数：12

    Examples
    --------
    股票软件上常再求一次MA
    >>> MA(MTM(CLOSE, 12), 6)

    """
    if real.ndim == 2:
        return DIFF(real, timeperiod)
    else:
        return ta.MOM(real, timeperiod=timeperiod)


def PSY(real, timeperiod=12):
    """PSY心理线

    Parameters
    ----------
    real
    timeperiod:int
        常用参数：12

    Examples
    --------
    股票软件上常再求一次MA
    >>> MA(PSY(CLOSE, 12), 6)

    """
    return COUNT(real > REF(real, 1), timeperiod) / timeperiod * 100


def DM(high, low, timeperiod=14):
    """Directional Movement方向动量

    WS_SUM威尔德平滑求和
    """
    if high.ndim == 2:
        HD = high - REF(high, 1)
        LD = REF(low, 1) - low
        # talib中是用的威尔德平滑
        PDM = WS_SUM(((HD > 0) & (HD > LD)) * HD, timeperiod)
        MDM = WS_SUM(((LD > 0) & (LD > HD)) * LD, timeperiod)
        return PDM, MDM
    else:
        return ta.PLUS_DM(high, low, timeperiod=timeperiod), ta.MINUS_DM(high, low, timeperiod=timeperiod)


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
    if close.ndim == 2:
        TRS = WS_SUM(TR(high, low, close), timeperiod)

        # 与talib相比多了一个数字，所以删除一下
        TRS = fill_notna(TRS, fill_value=np.nan, n=1)

        PDM, MDM = DM(high, low, timeperiod)
        PDI = PDM * 100 / TRS
        MDI = MDM * 100 / TRS
        return PDI, MDI
    else:
        return ta.PLUS_DI(high, low, close, timeperiod=timeperiod), ta.MINUS_DI(high, low, close, timeperiod=timeperiod)


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
    if high.ndim == 2:
        PDI, MDI = DI(high, low, close, timeperiod=timeperiod)
        ADX = SMA(ABS(PDI - MDI) / (PDI + MDI) * 100, timeperiod)
        # 这里timeperiod-1，才正好与talib对应
        ADXR = (ADX + REF(ADX, timeperiod - 1)) / 2
        return PDI, MDI, ADX, ADXR
    else:
        return (ta.PLUS_DI(high, low, close, timeperiod=timeperiod),
                ta.MINUS_DI(high, low, close, timeperiod=timeperiod),
                ta.ADX(high, low, close, timeperiod=timeperiod),
                ta.ADXR(high, low, close, timeperiod=timeperiod),
                )


def DMI_CN(high, low, close, timeperiod=14):
    # DI算法不同
    PDI, MDI = DI_CN(high, low, close, timeperiod=timeperiod)
    # ADX中的MA与SMA不同
    ADX = MA(ABS(PDI - MDI) / (PDI + MDI) * 100, timeperiod)
    # timeperiod与timeperiod-1不同
    ADXR = (ADX + REF(ADX, timeperiod)) / 2
    return PDI, MDI, ADX, ADXR


def TRIX(real, timeperiod=12):
    """三重指数平滑均线

    由EMA算法差异导致的不同
    """
    if real.ndim == 2:
        TR = EMA_1_PD(EMA_1_PD(EMA_1_PD(real, timeperiod), timeperiod), timeperiod)
        return ROC(TR, 1)
    else:
        # ta.set_compatibility(1)
        return ta.TRIX(real, timeperiod=timeperiod)
