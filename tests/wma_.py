import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import ta_cn.talib as ta
from ta_cn.slow import WMA

if __name__ == '__main__':
    # 准备数据
    h = np.random.rand(100000).reshape(-1, 500) + 10
    l = np.random.rand(100000).reshape(-1, 500)
    c = np.random.rand(100000).reshape(-1, 500)

    t1 = time.time()
    z1 = ta.WMA(c, timeperiod=10)
    t2 = time.time()
    z2 = WMA(c, timeperiod=10).values
    t3 = time.time()

    print(t2 - t1, t3 - t2)

    pd.DataFrame({'TA': z1[:, 0], 'MY': z2[:, 0]}).plot()
    pd.DataFrame({'MY': z2[:, 0], 'TA': z1[:, 0]}).plot()
    plt.show()
