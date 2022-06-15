import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import talib as ta
from talib import MA_Type

from ta_cn.utils import np_to_pd

a = np.random.rand(10000)


def EMA1(real, timeperiod=24):
    ta.set_compatibility(1)
    return ta.EMA(real, timeperiod=timeperiod)


def EMA2(real, timeperiod=24):
    ret = np_to_pd(real).ewm(span=timeperiod, min_periods=timeperiod, adjust=False).mean()
    return ret


def EMA3(real, timeperiod=24):
    ta.set_compatibility(0)
    return ta.EMA(real, timeperiod=timeperiod)


def EMA4(real, timeperiod=24):
    real = np_to_pd(real, copy=True)
    real[:timeperiod] = real[:timeperiod].rolling(window=timeperiod, min_periods=timeperiod).mean()
    ret = real.ewm(span=timeperiod, adjust=False).mean()
    return ret


def MACD1(real: pd.DataFrame, fastperiod=12, slowperiod=26, signalperiod=9):  # EMA的关系，S取120日，和雪球小数点2位相同
    macd, macdsignal, macdhist = ta.MACDEXT(real,
                                            fastperiod=fastperiod, fastmatype=MA_Type.EMA,
                                            slowperiod=slowperiod, slowmatype=MA_Type.EMA,
                                            signalperiod=signalperiod, signalmatype=MA_Type.EMA)
    # macd起始位不是按slowperiod-1，而是按slowperiod+signalperiod-2，可能是为了三个输出的起始位相同
    # talib中的MACD没有*2
    return macd, macdsignal, macdhist * 2


def MACD2(real: pd.DataFrame, fastperiod=12, slowperiod=26, signalperiod=9):  # EMA的关系，S取120日，和雪球小数点2位相同
    DIF = EMA2(real, fastperiod) - EMA2(real, slowperiod)
    DEA = EMA2(DIF, signalperiod)
    MACD = (DIF - DEA) * 2
    return DIF, DEA, MACD


if __name__ == '__main__':
    # funcs = ['MACD']
    # for func in funcs:
    #     print(func)
    #     t1 = time.time()
    #     r1 = MACD1(a)[0]
    #
    #     t2 = time.time()
    #     r2 = MACD2(a)[0]
    #     t3 = time.time()
    #
    #     print(t2 - t1, t3 - t2)
    #
    #     pd.DataFrame({'TA': r1, 'MY': r2}).plot()
    #     pd.DataFrame({'MY': r2, 'TA': r1}).plot()
    #     plt.show()

    # funcs = ['EMA']
    # for func in funcs:
    #     print(func)
    #     t1 = time.time()
    #     r1 = EMA1(a)
    #
    #     t2 = time.time()
    #     r2 = EMA2(a)
    #     t3 = time.time()
    #
    #     print(t2 - t1, t3 - t2)
    #
    #     pd.DataFrame({'TA': r1, 'MY': r2}).plot()
    #     pd.DataFrame({'MY': r2, 'TA': r1}).plot()
    #     plt.show()

    funcs = ['EMA']
    for func in funcs:
        print(func)
        t1 = time.time()
        r1 = EMA3(a)

        t2 = time.time()
        r2 = EMA4(a)
        t3 = time.time()

        print(t2 - t1, t3 - t2)

        pd.DataFrame({'TA': r1, 'MY': r2}).plot()
        pd.DataFrame({'MY': r2, 'TA': r1}).plot()
        plt.show()
