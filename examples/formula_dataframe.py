import pandas as pd

from ta_cn.imports.wide import ATR
from ta_cn.utils import np_to_pd

pd._testing._N = 250
pd._testing._K = 30
h = pd._testing.makeTimeDataFrame() + 10
l = pd._testing.makeTimeDataFrame()
c = pd._testing.makeTimeDataFrame()

r = ATR(h, l, c, 10)
# 返回的数据可能是np.ndarray
print(r.raw())

# 可以再封装回pd.DataFrame
d = np_to_pd(r.raw(), copy=False, index=c.index, columns=c.columns)
print(d.iloc[-5:])
