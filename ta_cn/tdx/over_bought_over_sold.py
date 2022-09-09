from talib import MA_Type

from ta_cn import talib as ta
from ta_cn.tdx.reference import TR
from ta_cn.wq.time_series import ts_min as LLV
from ta_cn.wq.time_series import ts_max as HHV
from ta_cn.wq.time_series import ts_mean as MA
from ta_cn.wq.arithmetic import mean as MEAN
from ta_cn.wq.time_series import ts_delay as REF
from ta_cn.talib import set_compatibility, TA_COMPATIBILITY_DEFAULT, TA_COMPATIBILITY_METASTOCK

_ta1d = ta.init(mode=1, skipna=False)
_ta2d = ta.init(mode=2, skipna=False)


def ATR_CN(high, low, close, timeperiod):
    """ATR真实波幅N日平均

    ATR_CN(high, low, close, timeperiod=14)

    talib的ATR算法类似于EMA，所以要重写此处才与中国ATR相同
    """
    return MA(TR(high, low, close), timeperiod)


def BIAS(real, timeperiod):
    """BIAS乖离率

    BIAS(real, timeperiod=6)

    Parameters
    ----------
    real
    timeperiod:int
        常用参数：6,12,24

    """
    return (real / MA(real, timeperiod) - 1) * 100


def KDJ(high, low, close, fastk_period, M1, M2):
    """KDJ指标

    KDJ(high, low, close, fastk_period=9, M1=3, M2=3)

    talib中EMA的参数用法不同
    """
    set_compatibility(TA_COMPATIBILITY_METASTOCK)

    K, D = _ta2d.STOCH(high, low, close,
                       fastk_period=fastk_period,
                       slowk_period=(M1 * 2 - 1), slowk_matype=MA_Type.EMA,
                       slowd_period=(M2 * 2 - 1), slowd_matype=MA_Type.EMA)

    J = K * 3 - D * 2
    return K, D, J


def ROC(real, timeperiod=12):  # 变动率指标
    """ROC变动率指标

    Parameters
    ----------
    real
    timeperiod:int
        常用参数：12

    Examples
    --------
    股票软件上常再求一次MA
    >>> MA(ROC(CLOSE, 12), 6)

    """
    if real.ndim == 2:
        return (real / REF(real, timeperiod) - 1) * 100
    else:
        return _ta1d.ROC(real, timeperiod=timeperiod)


def TYPPRICE(high, low, close):
    """典型价格。高低收的平均值"""
    if close.ndim == 2:
        return MEAN(high, low, close)
    else:
        return _ta1d.TYPPRICE(high, low, close)


def MEDPRICE(high, low):
    """中间价格。高低平均值"""
    if high.ndim == 2:
        return MEAN(high, low)
    else:
        return _ta1d.MEDPRICE(high, low)


def WR(high, low, close, timeperiod=10):
    """W&R威廉指标

    Parameters
    ----------
    high
    low
    close
    timeperiod: int
        常用参数：10, 6

    Returns
    -------

    """

    if close.ndim == 2:
        hh = HHV(high, timeperiod)
        ll = LLV(low, timeperiod)
        return (hh - close) / (hh - ll) * 100
    else:
        return _ta1d.WILLR(high, low, close, timeperiod=timeperiod)


def RSI(real, timeperiod=24):
    """RSI指标"""
    # 如果设置成1，将会多一个数字
    set_compatibility(TA_COMPATIBILITY_DEFAULT)

    return _ta2d.RSI(real, timeperiod=timeperiod)
