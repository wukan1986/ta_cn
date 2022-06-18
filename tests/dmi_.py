import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ta_cn.slow import DMI as DMI2
from ta_cn.trend import DMI as DMI1

if __name__ == '__main__':
    # 准备数据
    h = np.random.rand(1000).reshape(-1, 5) + 10
    l = np.random.rand(1000).reshape(-1, 5)
    c = np.random.rand(1000).reshape(-1, 5)

    h[:20, -1] = np.nan
    l[:20, -1] = np.nan
    c[:20, -1] = np.nan

    t1 = time.time()
    z1 = DMI1(h, l, c, 3)[3]  # 查看的是ADXR
    t2 = time.time()
    z2 = DMI2(h, l, c, 3)[3].values
    t3 = time.time()

    print(t2 - t1, t3 - t2)

    pd.DataFrame({'TA': z1[:, -1], 'MY': z2[:, -1]}).plot()
    pd.DataFrame({'MY': z2[:, -1], 'TA': z1[:, -1]}).plot()

    plt.show()
