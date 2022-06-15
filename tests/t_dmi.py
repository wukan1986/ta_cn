import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import talib as ta

from ta_cn import REF, TR, ABS, fill_notna
from ta_cn.ema import WS_SUM, SMA


def DM1(high, low, timeperiod=14):  # 能量潮指标
    # 内部在timeperiod计算时用了快速的方法，所以与我们自己算的有误差
    return ta.PLUS_DM(high, low, timeperiod=timeperiod), ta.MINUS_DM(high, low, timeperiod=timeperiod)


def DM2(high, low, timeperiod=14):  # 能量潮指标
    HD = high - REF(high, 1)
    LD = REF(low, 1) - low
    PDM = WS_SUM(((HD > 0) & (HD > LD)) * HD, timeperiod)
    MDM = WS_SUM(((LD > 0) & (LD > HD)) * LD, timeperiod)
    return PDM, MDM


def DI1(high, low, close, timeperiod=14):
    return ta.PLUS_DI(high, low, close, timeperiod=timeperiod), ta.MINUS_DI(high, low, close, timeperiod=timeperiod)


def DI2(high, low, close, timeperiod=14):
    """Directional Indicator方向指标"""
    TRS = WS_SUM(TR(high, low, close), timeperiod)

    # 与talib相比多了一个数字，所以删除一下
    #TRS = fill_notna(TRS, fill_value=np.nan, n=1)

    PDM, MDM = DM2(high, low, timeperiod)
    PDI = PDM * 100 / TRS
    MDI = MDM * 100 / TRS
    return PDI, MDI


def ADX1(high, low, close, timeperiod=14):
    return ta.ADX(high, low, close, timeperiod=timeperiod),


def ADX2(high, low, close, timeperiod=14):
    PDI, MDI = DI2(high, low, close, timeperiod=timeperiod)
    ADX = SMA(ABS(PDI - MDI) / (PDI + MDI) * 100, timeperiod)
    ADXR = (ADX + REF(ADX, timeperiod)) / 2
    return ADX,


def ADXR1(high, low, close, timeperiod=14):
    return ta.ADXR(high, low, close, timeperiod=timeperiod),


def ADXR2(high, low, close, timeperiod=14):
    PDI, MDI = DI2(high, low, close, timeperiod=timeperiod)
    ADX = SMA(ABS(PDI - MDI) / (PDI + MDI) * 100, timeperiod)
    ADX = ta.ADX(high, low, close, timeperiod=14)
    ADXR = (ADX + REF(ADX, timeperiod-1)) / 2
    return ADXR,


a = np.random.rand(10000) + 10
b = np.random.rand(10000)
c = np.random.rand(10000)

if __name__ == '__main__':
    funcs = ['OBV']
    for func in funcs:
        print(func)

        t1 = time.time()
        # r1 = DM1(a, b)[0]
        # r1 = DI1(a, b, c)[0]
        # r1 = ADX1(a, b, c)[0]
        r1 = ADXR1(a, b, c)[0]
        r1 = pd.Series(r1)

        t2 = time.time()
        # r2 = DM2(a, b)[0]
        # r2 = DI2(a, b, c)[0]
        # r2 = ADX2(a, b, c)[0]
        r2 = ADXR2(a, b, c)[0]

        t3 = time.time()

        print(t2 - t1, t3 - t2)

        pd.DataFrame({'TA': r1, 'MY': r2}).plot()
        pd.DataFrame({'MY': r2, 'TA': r1}).plot()
        plt.show()
