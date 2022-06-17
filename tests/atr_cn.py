import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ta_cn.over_bought_over_sold import ATR_CN as ATR_CN1
from ta_cn.slow import ATR_CN as ATR_CN2

if __name__ == '__main__':
    # 准备数据
    h = np.random.rand(10000000).reshape(-1, 50000) + 10
    l = np.random.rand(10000000).reshape(-1, 50000)
    c = np.random.rand(10000000).reshape(-1, 50000)

    t1 = time.time()
    z1 = ATR_CN1(h, l, c)
    t2 = time.time()
    z2 = ATR_CN2(h, l, c)
    t3 = time.time()

    print(t2 - t1, t3 - t2)

    pd.DataFrame({'TA': z1[:, -1], 'MY': z2[:, -1]}).plot()
    pd.DataFrame({'MY': z2[:, -1], 'TA': z1[:, -1]}).plot()
    plt.show()
