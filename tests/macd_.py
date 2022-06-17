import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ta_cn import TA_SET_COMPATIBILITY
from ta_cn.slow import MACD_CN
from ta_cn.ta import TA_SET_COMPATIBILITY_ENABLE
from ta_cn.trend import MACD

if __name__ == '__main__':
    TA_SET_COMPATIBILITY_ENABLE(True)
    TA_SET_COMPATIBILITY(1)
    TA_SET_COMPATIBILITY_ENABLE(False)

    # 准备数据
    h = np.random.rand(100000).reshape(-1, 500) + 10
    l = np.random.rand(100000).reshape(-1, 500)
    c = np.random.rand(100000).reshape(-1, 500)

    t1 = time.time()
    z1 = MACD(c)[-1]
    t2 = time.time()
    z2 = MACD_CN(c)[-1].values
    t3 = time.time()

    print(t2 - t1, t3 - t2)

    pd.DataFrame({'TA': z1[:, -1], 'MY': z2[:, -1]}).plot()
    pd.DataFrame({'MY': z2[:, -1], 'TA': z1[:, -1]}).plot()
    plt.show()
