import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import talib as ta

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
