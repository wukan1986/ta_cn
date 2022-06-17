import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import ta_cn.talib as ta
from ta_cn.slow import ATR

if __name__ == '__main__':
    # 准备数据
    h = np.random.rand(10000000).reshape(-1, 50000) + 10
    l = np.random.rand(10000000).reshape(-1, 50000)
    c = np.random.rand(10000000).reshape(-1, 50000)

    t1 = time.time()
    z1 = ta.ATR(h, l, c)
    t2 = time.time()
    z2 = ATR(h, l, c).values
    t3 = time.time()

    print(t2 - t1, t3 - t2)

    pd.DataFrame({'TA': z1[:, -1], 'MY': z2[:, -1]}).plot()
    pd.DataFrame({'MY': z2[:, -1], 'TA': z1[:, -1]}).plot()
    plt.show()
