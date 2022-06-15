import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import talib as ta

from ta_cn import MAX, REF, ABS
from ta_cn.ema import SMA

a = np.random.rand(10000)


def RSI0(real, timeperiod=24):
    ta.set_compatibility(0)
    return ta.RSI(real, timeperiod=timeperiod)


def RSI1(real, timeperiod=24):
    # 多算了一个值放在了最前边
    ta.set_compatibility(1)
    return ta.RSI(real, timeperiod=timeperiod)


def RSI2(real, timeperiod=24):  # RSI指标,和通达信小数点2位相同
    DIF = real - REF(real, 1)
    return SMA(MAX(DIF, 0), timeperiod, 1) / SMA(ABS(DIF), timeperiod, 1) * 100


if __name__ == '__main__':
    funcs = ['RSI']
    for func in funcs:
        print(func)
        t1 = time.time()
        r1 = RSI0(a)

        t2 = time.time()
        r2 = RSI2(a)
        t3 = time.time()

        print(t2 - t1, t3 - t2)

        pd.DataFrame({'TA': r1, 'MY': r2}).plot()
        pd.DataFrame({'MY': r2, 'TA': r1}).plot()
        plt.show()

        ta.PPO
