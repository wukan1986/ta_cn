import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ta_cn.talib import set_compatibility_enable, TA_COMPATIBILITY_METASTOCK, set_compatibility
from ta_cn.slow import TRIX_CN
import ta_cn.talib as ta

if __name__ == '__main__':
    set_compatibility_enable(True)
    set_compatibility(TA_COMPATIBILITY_METASTOCK)
    set_compatibility_enable(False)
    # 准备数据
    h = np.random.rand(100000).reshape(-1, 500) + 10
    l = np.random.rand(100000).reshape(-1, 500)
    c = np.random.rand(100000).reshape(-1, 500)

    c[:20, -1] = np.nan

    t1 = time.time()

    z1 = ta.TRIX(c, timeperiod=10)
    t2 = time.time()
    z2 = TRIX_CN(c, timeperiod=10)
    t3 = time.time()

    print(t2 - t1, t3 - t2)

    pd.DataFrame({'TA': z1[:, -1], 'MY': z2[:, -1]}).plot()
    pd.DataFrame({'MY': z2[:, -1], 'TA': z1[:, -1]}).plot()
    plt.show()
