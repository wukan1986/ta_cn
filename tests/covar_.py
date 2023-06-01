import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ta_cn.nb import numpy_rolling_apply_1, _rolling_func_2_1_nb, _cov_nb
from ta_cn.utils import np_to_pd, pd_to_np


def COVAR(real0, real1, timeperiod=30):
    return numpy_rolling_apply_1([pd_to_np(real0), pd_to_np(real1)],
                                 timeperiod, _rolling_func_2_1_nb, _cov_nb)


# 移动相关系数
def correlation(x, y, window=30):
    return np_to_pd(x).rolling(window).corr(np_to_pd(y))


# 移动协方差
def covariance(x, y, window=30):
    return np_to_pd(x).rolling(window).cov(np_to_pd(y))


if __name__ == '__main__':
    # 准备数据
    h = np.random.rand(100000).reshape(-1, 500) + 10
    l = np.random.rand(100000).reshape(-1, 500)

    z1 = COVAR(h, l)
    t1 = time.time()
    z1 = COVAR(h, l)
    t2 = time.time()
    z2 = covariance(h, l).values
    t3 = time.time()
    print(t2 - t1, t3 - t2)

    pd.DataFrame({'TA': z1[:, -1], 'MY': z2[:, -1]}).plot()
    pd.DataFrame({'MY': z2[:, -1], 'TA': z1[:, -1]}).plot()
    plt.show()
