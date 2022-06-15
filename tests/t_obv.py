import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import talib as ta

from ta_cn import SGN, DIFF, SUM


def OBV1(real, volume):  # 能量潮指标
    return ta.OBV(real, volume)


def OBV2(real, volume):  # 能量潮指标
    S = SGN(DIFF(real))
    # 中国区第一天当成0，改成1就与talib一样了
    S[0] = 1
    # 同花顺最后会除10000，但东方财富没有除
    return SUM(S * volume, 0)


a = np.random.rand(10000)
b = np.random.rand(10000) * 100

if __name__ == '__main__':
    funcs = ['OBV']
    for func in funcs:
        print(func)
        t2 = time.time()
        r2 = OBV1(a, b)
        t3 = time.time()

        t1 = time.time()
        r1 = OBV2(a, b)

        print(t2 - t1, t3 - t2)

        pd.DataFrame({'TA': r1, 'MY': r2}).plot()
        pd.DataFrame({'MY': r2, 'TA': r1}).plot()
        plt.show()
