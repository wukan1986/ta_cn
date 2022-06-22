import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ta_cn.ema import EXPMEMA, EMA_0_TA, EMA_1_TA, EMA_1_PD
from ta_cn.ta import TA_SET_COMPATIBILITY_ENABLE

if __name__ == '__main__':
    TA_SET_COMPATIBILITY_ENABLE(True)

    # 准备数据
    h = np.random.rand(100000).reshape(-1, 500) + 10
    l = np.random.rand(100000).reshape(-1, 500)
    c = np.random.rand(100000).reshape(-1, 500)

    c[:20, -1] = np.nan
    z2 = EXPMEMA(c)

    t1 = time.time()
    z1 = EMA_0_TA(c)
    t2 = time.time()
    z2 = EXPMEMA(c)
    t3 = time.time()

    print(t2 - t1, t3 - t2)

    pd.DataFrame({'TA': z1[:, -1], 'MY': z2[:, -1]}).plot()
    pd.DataFrame({'MY': z2[:, -1], 'TA': z1[:, -1]}).plot()
    # plt.show()

    t1 = time.time()
    z1 = EMA_1_TA(c)
    t2 = time.time()
    z2 = EMA_1_PD(c)
    t3 = time.time()

    print(t2 - t1, t3 - t2)

    pd.DataFrame({'TA': z1[:, -1], 'MY': z2[:, -1]}).plot()
    pd.DataFrame({'MY': z2[:, -1], 'TA': z1[:, -1]}).plot()
    plt.show()
