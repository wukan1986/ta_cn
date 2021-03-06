import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import ta_cn.talib as ta
from ta_cn.slow import MFI

if __name__ == '__main__':
    # 准备数据
    h = np.random.rand(10000000).reshape(-1, 50000) + 10
    l = np.random.rand(10000000).reshape(-1, 50000)
    c = np.random.rand(10000000).reshape(-1, 50000)
    v = np.random.rand(10000000).reshape(-1, 50000) * 1000

    c[:20, -1] = np.nan

    t1 = time.time()
    z1 = ta.MFI(h, l, c, v)
    t2 = time.time()
    z2 = MFI(h, l, c, v)
    t3 = time.time()

    print(t2 - t1, t3 - t2)

    pd.DataFrame({'TA': z1[:, 0], 'MY': z2[:, 0]}).plot()
    pd.DataFrame({'MY': z2[:, 0], 'TA': z1[:, 0]}).plot()
    plt.show()
