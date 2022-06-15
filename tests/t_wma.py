import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import talib as ta

from ta_cn import np_to_pd

a = np.random.rand(10000)


def WMA1(real, timeperiod=10):
    return ta.WMA(real, timeperiod)


def WMA2(real, timeperiod=10):
    def func(x):
        # 复制于MyTT,比tqsdk中tafunc中计算要快
        return x[::-1].cumsum().sum() * 2 / timeperiod / (timeperiod + 1)

    return np_to_pd(real).rolling(timeperiod).apply(func, raw=True)


if __name__ == '__main__':
    funcs = ['WMA']
    for func in funcs:
        print(func)
        t1 = time.time()
        r1 = WMA1(a)

        t2 = time.time()
        r2 = WMA2(a)
        t3 = time.time()

        print(t2 - t1, t3 - t2)

        pd.DataFrame({'TA': r1, 'MY': r2}).plot()
        pd.DataFrame({'MY': r2, 'TA': r1}).plot()
        plt.show()
