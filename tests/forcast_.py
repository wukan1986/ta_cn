import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import talib as ta

# def FORCAST(S, N=14):  # 返回S序列N周期回线性回归后的预测值， jqz1226改进成序列出
#     return pd.DataFrame(S).rolling(N).apply(lambda x: np.polyval(np.polyfit(range(N), x, deg=1), N - 1), raw=True)
from ta_cn.statistics import FORCAST

if __name__ == '__main__':
    # 准备数据
    h = np.random.rand(100000).reshape(-1, 500) + 10
    l = np.random.rand(100000).reshape(-1, 500)
    c = np.random.rand(100000).reshape(-1, 500)

    c[:20, -1] = np.nan
    # 先执行一次让numba编译

    t1 = time.time()
    z1 = ta.LINEARREG(c)
    t2 = time.time()
    z2 = FORCAST(c).values
    t3 = time.time()

    print(t2 - t1, t3 - t2)

    pd.DataFrame({'TA': z1[:, -1], 'MY': z2[:, -1]}).plot()
    pd.DataFrame({'MY': z2[:, -1], 'TA': z1[:, -1]}).plot()
    plt.show()

    FORCAST
