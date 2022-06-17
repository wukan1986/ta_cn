import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ta_cn.slow import DI as DI2
from ta_cn.slow import DM as DM2
from ta_cn.slow import DMI as DMI2
from ta_cn.trend import DI as DI1
from ta_cn.trend import DM as DM1
from ta_cn.trend import DMI as DMI1

if __name__ == '__main__':
    # 准备数据
    h = np.random.rand(1000).reshape(-1, 5) + 10
    l = np.random.rand(1000).reshape(-1, 5)
    c = np.random.rand(1000).reshape(-1, 5)

    t1 = time.time()
    z1 = DM1(h, l)[0]
    y1 = DI1(h, l, c)[0]
    x1 = DMI1(h, l, c)[3]
    t2 = time.time()
    z2 = DM2(h, l)[0].values
    y2 = DI2(h, l, c)[0].values
    x2 = DMI2(h, l, c)[3].values
    t3 = time.time()

    print(t2 - t1, t3 - t2)

    pd.DataFrame({'TA': z1[:, -1], 'MY': z2[:, -1]}).plot()
    pd.DataFrame({'MY': z2[:, -1], 'TA': z1[:, -1]}).plot()

    pd.DataFrame({'TA': y1[:, -1], 'MY': y2[:, -1]}).plot()
    pd.DataFrame({'MY': y2[:, -1], 'TA': y1[:, -1]}).plot()

    pd.DataFrame({'TA': x1[:, -1], 'MY': x2[:, -1]}).plot()
    pd.DataFrame({'MY': x2[:, -1], 'TA': x1[:, -1]}).plot()

    plt.show()
