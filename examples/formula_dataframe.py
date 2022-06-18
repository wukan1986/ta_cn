import pandas as pd

from ta_cn.imports import *
from ta_cn.utils import np_to_pd

pd._testing._N = 250
pd._testing._K = 30
h = pd._testing.makeTimeDataFrame() + 10
l = pd._testing.makeTimeDataFrame()
c = pd._testing.makeTimeDataFrame()

r = ATR_CN(h, l, c)
# 返回的数据可能是np.ndarray
print(r[-5:])

# 可以再封装回pd.DataFrame
d = np_to_pd(r, copy=False, index=c.index, columns=c.columns)
print(d.iloc[-5:])
