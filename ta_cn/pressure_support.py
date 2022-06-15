import pandas as pd
import talib as ta

from .reference import MA
from .statistics import STDP


def BOLL(real: pd.DataFrame, timeperiod=20, nbdevup=2, nbdevdn=2):
    """BOLL指标，布林带

    使用总体标准差

    References
    ----------
    https://en.wikipedia.org/wiki/Bollinger_Bands

    """
    if real.ndim == 2:
        MID = MA(real, timeperiod)
        # 这里是总体标准差，值比样本标准差小。部分软件使用样本标准差是错误的，
        _std = STDP(real, timeperiod)
        UPPER = MID + _std * nbdevup
        LOWER = MID - _std * nbdevdn
        return UPPER, MID, LOWER
    else:
        return ta.BBANDS(real, timeperiod=timeperiod, nbdevup=nbdevup, nbdevdn=nbdevdn)
