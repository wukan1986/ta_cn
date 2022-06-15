import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import talib as ta

from ta_cn import TYP, SUM, REF
from ta_cn.nb import fill_notna

# .reshape(-1, 1)
a = np.random.rand(10000) + 10
b = np.random.rand(10000)
c = np.random.rand(10000)
d = np.random.rand(10000) * 10
d[:10] = np.nan


def MFI1(high, low, close, volume, timeperiod=14):
    ta.set_compatibility(1)
    return ta.MFI(high, low, close, volume, timeperiod=timeperiod)


def MFI2(high, low, close, volume, timeperiod=14):
    tp = TYP(high, low, close)
    tpv = tp * volume
    # 比TALIB结果多一个数字，通过置空实现与TA-LIB完全一样
    tpv = fill_notna(tpv, fill_value=np.nan, n=1)

    is_raising = tp > REF(tp, 1)
    pos_sum = SUM(is_raising * tpv, timeperiod)
    neg_sum = SUM(~is_raising * tpv, timeperiod)
    return 100 * pos_sum / (pos_sum + neg_sum)


if __name__ == '__main__':

    funcs = ['MFI1']
    for func in funcs:
        print(func)
        t1 = time.time()
        r1 = MFI1(a, b, c, d)

        t2 = time.time()
        r2 = MFI2(a, b, c, d)
        t3 = time.time()

        print(t2 - t1, t3 - t2)

        pd.DataFrame({'TA': r1, 'MY': r2}).plot()
        pd.DataFrame({'MY': r2, 'TA': r1}).plot()
        plt.show()
