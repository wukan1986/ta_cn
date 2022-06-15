import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import talib as ta

from ta_cn import ROC, EMA_1_PD

a = np.random.rand(10000)


def TRIX1(real, timeperiod=12):
    ta.set_compatibility(1)
    return ta.TRIX(real, timeperiod=timeperiod)


def TRIX2(real, timeperiod=12):
    TR = EMA_1_PD(EMA_1_PD(EMA_1_PD(real, timeperiod), timeperiod), timeperiod)
    return ROC(TR, 1)


if __name__ == '__main__':

    funcs = ['TRIX']
    for func in funcs:
        print(func)
        t1 = time.time()
        r1 = TRIX1(a)

        t2 = time.time()
        r2 = TRIX2(a)
        t3 = time.time()

        print(t2 - t1, t3 - t2)

        pd.DataFrame({'TA': r1, 'MY': r2}).plot()
        pd.DataFrame({'MY': r2, 'TA': r1}).plot()
        plt.show()
