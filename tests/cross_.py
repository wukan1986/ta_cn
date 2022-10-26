import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas._testing import assert_numpy_array_equal

from ta_cn.tdx.logical import CROSS

names = ['rf']
dates = pd.date_range(start='2017-01-01', end='2017-12-31', freq=pd.tseries.offsets.BDay())
n = len(dates)
rdf = pd.DataFrame(
    np.zeros((n, len(names))),
    index=dates,
    columns=names
)

np.random.seed(1)
rdf['rf'] = 0.

pdf = 100 * np.cumprod(1 + rdf)

factor = rdf.copy()
factor[:] = 1.0
factor[:][-100:] = 1.1
factor[:][-50:] = 1.5

close_h = pdf * factor
close_q = pdf * (factor / factor.iloc[-1])


def calc(close):
    # 不同的复权方法，结果不同，已经修正

    # 多了两点
    ma5 = close.rolling(10).mean()
    ma10 = close.rolling(20).mean()

    # 少了一点
    # ma5 = ta.MA(close.iloc[:, 0], 10)
    # ma10 = ta.MA(close.iloc[:, 0], 20)

    r = CROSS(ma5, ma10)

    df = pd.DataFrame()
    df['CLOSE'] = close
    df['CROSS'] = r.astype(float)
    df['MA5'] = ma5
    df['MA10'] = ma10

    return df


a1 = calc(close_h)  # 出现了两个毛刺，原来是精度差异导致
a1.plot(secondary_y=['CROSS'])

a2 = calc(close_q)  # 换算法后又少一个点
a2.plot(secondary_y=['CROSS'])

assert_numpy_array_equal(a1['CROSS'].values, a2['CROSS'].values)

plt.show()

#
