import numpy as np
import pandas as pd

from ta_cn.performance import weighted_index, ic, ir, ic_decay
from ta_cn.split import top_k, quantile_n

# 因子值
f = np.random.rand(10000).reshape(-1, 500)
# 持有1期收益
r = np.random.rand(10000).reshape(-1, 500) / 100

ics = ic(f, r)
print(ics)
print(ir(ics))
print(ic_decay(f, r).mean())

# 前50,前100，前200，分三组的净值
d = {}
topK = top_k(-f, bins=[0, 50, 100, 200])
for k, v in topK.items():
    d[k] = weighted_index(~np.isnan(v), returns=r, need_one=True)

df = pd.DataFrame(d)
print(df)

# 分十组的净值
d = {}
qN = quantile_n(f, n=10)
for k, v in qN.items():
    d[k] = weighted_index(~np.isnan(v), returns=r, need_one=True)

df = pd.DataFrame(d)
print(df)
