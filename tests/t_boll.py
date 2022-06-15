import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import talib as ta

from ta_cn import MA
from ta_cn.statistics import STDP

a = np.random.rand(10000)


def BOLL1(real: pd.DataFrame, timeperiod=20, nbdevup=2, nbdevdn=2):
    return ta.BBANDS(real, timeperiod=timeperiod, nbdevup=nbdevup, nbdevdn=nbdevdn)


def BOLL2(real: pd.DataFrame, timeperiod=20, nbdevup=2, nbdevdn=2):
    """BOLL指标，布林带"""
    MID = MA(real, timeperiod)
    _std = STDP(real, timeperiod)  # 这里是总体标准差
    UPPER = MID + _std * nbdevup
    LOWER = MID - _std * nbdevdn
    return UPPER, MID, LOWER


if __name__ == '__main__':
    funcs = ['BOLL']
    for func in funcs:
        print(func)
        t1 = time.time()
        r1 = BOLL1(a)[0]

        t2 = time.time()
        r2 = BOLL2(a)[0]
        t3 = time.time()

        print(t2 - t1, t3 - t2)

        pd.DataFrame({'TA': r1, 'MY': r2}).plot()
        pd.DataFrame({'MY': r2, 'TA': r1}).plot()
        plt.show()
