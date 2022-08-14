from talib import MA_Type

import ta_cn.talib as ta
from ta_cn.talib import set_compatibility, TA_COMPATIBILITY_METASTOCK
from .maths import MEAN
from .reference import COUNT, REF, DIFF, MA

_ta1d = ta.init(mode=1, skipna=False)
_ta2d = ta.init(mode=2, skipna=False)


def BBI(real, timeperiod1: int, timeperiod2: int, timeperiod3: int, timeperiod4: int):
    """BBI多空指标

    BBI(real, timeperiod1=3, timeperiod2=6, timeperiod3=12, timeperiod4=24)

    """
    return MEAN(MA(real, timeperiod1),
                MA(real, timeperiod2),
                MA(real, timeperiod3),
                MA(real, timeperiod4))


def DPO(real, timeperiod: int):
    """DPO区间震荡线

    DPO(real, timeperiod=20)

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


def MACD(real, fastperiod: int, slowperiod: int, signalperiod: int):
    """MACD指标

    MACD(real, fastperiod=12, slowperiod=26, signalperiod=9)

    """
    set_compatibility(TA_COMPATIBILITY_METASTOCK)

    macd, macdsignal, macdhist = _ta2d.MACDEXT(real,
                                               fastperiod=fastperiod, fastmatype=MA_Type.EMA,
                                               slowperiod=slowperiod, slowmatype=MA_Type.EMA,
                                               signalperiod=signalperiod, signalmatype=MA_Type.EMA)

    # macd起始位不是按slowperiod-1，而是按slowperiod+signalperiod-2，可能是为了三个输出的起始位相同
    # talib中的MACD没有*2
    return macd, macdsignal, macdhist * 2


def MTM(real, timeperiod: int):
    """MTM动量指标

    MTM(real, timeperiod=12)

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
        return _ta1d.MOM(real, timeperiod=timeperiod)


def PSY(real, timeperiod: int):
    """PSY心理线

    PSY(real, timeperiod=12)

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


def DM(high, low, timeperiod):
    """Directional Movement方向动量

    DM(high, low, timeperiod=14)

    WS_SUM威尔德平滑求和
    """
    return _ta2d.PLUS_DM(high, low, timeperiod=timeperiod), _ta2d.MINUS_DM(high, low, timeperiod=timeperiod)


def DI(high, low, close, timeperiod: int):
    """Directional Indicator方向指标

    DI(high, low, close, timeperiod=14)
    """
    return _ta2d.PLUS_DI(high, low, close, timeperiod=timeperiod), _ta2d.MINUS_DI(high, low, close,
                                                                                  timeperiod=timeperiod)


def DMI(high, low, close, timeperiod: int):
    """趋向指标

    DMI(high, low, close, timeperiod=14)
    """
    return (_ta2d.PLUS_DI(high, low, close, timeperiod=timeperiod),
            _ta2d.MINUS_DI(high, low, close, timeperiod=timeperiod),
            _ta2d.ADX(high, low, close, timeperiod=timeperiod),
            _ta2d.ADXR(high, low, close, timeperiod=timeperiod),
            )


def TRIX(real, timeperiod: int):
    """三重指数平滑均线

    TRIX(real, timeperiod=12)

    由EMA算法差异导致的不同
    """
    set_compatibility(TA_COMPATIBILITY_METASTOCK)

    return _ta2d.TRIX(real, timeperiod=timeperiod)
