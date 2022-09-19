import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ta_cn.slow import _AVEDEV as AVEDEV2
from ta_cn.tdx.statistics import AVEDEV as AVEDEV1

if __name__ == '__main__':
    # 准备数据
    h = np.random.rand(100000).reshape(-1, 500) + 10
    l = np.random.rand(100000).reshape(-1, 500)
    c = np.random.rand(100000).reshape(-1, 500)

    c[:20, -1] = np.nan
    # 先执行一次让numba编译
    z1 = AVEDEV1(c)
    t1 = time.time()
    z1 = AVEDEV1(c)
    t2 = time.time()
    z2 = AVEDEV2(c).values
    t3 = time.time()

    print(t2 - t1, t3 - t2)

    pd.DataFrame({'TA': z1[:, -1], 'MY': z2[:, -1]}).plot()
    pd.DataFrame({'MY': z2[:, -1], 'TA': z1[:, -1]}).plot()
    plt.show()
