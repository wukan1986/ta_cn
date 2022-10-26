import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import talib as ta
from pandas._testing import assert_series_equal

from ta_cn import EPSILON
from ta_cn.tdx.logical import CROSS
from ta_cn.wq.arithmetic import divide
from ta_cn.wq.transformational import tail

names = ['foo', 'bar', 'rf']
names = ['rf']
dates = pd.date_range(start='2017-01-01', end='2017-12-31', freq=pd.tseries.offsets.BDay())
n = len(dates)
rdf = pd.DataFrame(
    np.zeros((n, len(names))),
    index=dates,
    columns=names
)

np.random.seed(1)
# rdf['foo'] = np.random.normal(loc=0.1 / n, scale=0.2 / np.sqrt(n), size=n)
# rdf['bar'] = np.random.normal(loc=0.04 / n, scale=0.05 / np.sqrt(n), size=n)
rdf['rf'] = 0.

pdf = 100 * np.cumprod(1 + rdf)

factor = rdf.copy()
factor[:] = 1.0
factor[:][-100:] = 1.1
factor[:][-50:] = 1.5

close_h = pdf * factor
close_q = pdf * (factor / factor.iloc[-1])


def calc(close):
    # STDDEV与收盘价的比结果是一样的，但VAR与close的比就不一样了
    # 不过VAR与close**2的二次方是一样的
    ma5 = ta.VAR(close.iloc[:, 0], 10)
    ma10 = close.iloc[:, 0]**2

    ma5 = tail(ma5, lower=-EPSILON, upper=EPSILON, newval=0)

    r = CROSS(ma5, ma10)

    df = pd.DataFrame()
    df['CLOSE'] = close
    df['CROSS'] = r.astype(float)
    df['MA5'] = ma5
    df['MA10'] = ma10
    df['5/10'] = divide(ma5, ma10)

    return df


a2 = calc(close_q)  # 换算法后又少一个点
a2.plot(secondary_y=['CROSS', '5/10'])

a1 = calc(close_h)  # 出现了两个毛刺，原来是精度差异导致
a1.plot(secondary_y=['CROSS', '5/10'])

plt.show()

assert_series_equal(a1['5/10'], a2['5/10'])
