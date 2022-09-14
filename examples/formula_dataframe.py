import pandas as pd

from ta_cn.imports.wide import ATR
from ta_cn.utils import np_to_pd
from ta_cn.utils_wide import WArr

pd._testing._N = 250
pd._testing._K = 30
h = pd._testing.makeTimeDataFrame() + 10
l = pd._testing.makeTimeDataFrame()
c = pd._testing.makeTimeDataFrame()

# 数据需要封装成特殊对象，实现NaN的堆叠和还原
h_ = WArr.from_array(h, direction='down')
l_ = WArr.from_array(l, direction='down')
c_ = WArr.from_array(c, direction='down')

r = ATR(h_, l_, c_, 10)
# 返回的数据可能是np.ndarray
print(r.raw())

# 可以再封装回pd.DataFrame
d = np_to_pd(r.raw(), copy=False, index=c.index, columns=c.columns)
print(d.iloc[-5:])
