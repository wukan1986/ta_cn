import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import ta_cn.talib as ta
from ta_cn.tdx.volume import OBV

if __name__ == '__main__':
    # 准备数据
    h = np.random.rand(10000000).reshape(-1, 50000) + 10
    l = np.random.rand(10000000).reshape(-1, 50000)
    c = np.random.rand(10000000).reshape(-1, 50000)
    v = np.random.rand(10000000).reshape(-1, 50000) * 1000

    c[:20, -1] = np.nan
    v[:20, -1] = np.nan

    t1 = time.time()
    z1 = ta.OBV(c, v)
    t2 = time.time()
    z2 = OBV(c, v, 1)
    t3 = time.time()

    print(t2 - t1, t3 - t2)

    pd.DataFrame({'TA': z1[:, -1], 'MY': z2[:, -1]}).plot()
    pd.DataFrame({'MY': z2[:, -1], 'TA': z1[:, -1]}).plot()
    plt.show()
