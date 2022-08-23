"""
本示例使用的是1期收益率*1期持仓权重。有以下注意事项：
1. 收益率是每次持有的时间。如持有5天，则将第5天价格除以第1天价格，得到的收益率移动到对应位置
2. 持有期不能重叠，否则结果错误
3. 只能用在做多场景。做空场景下复利结果有误差，

错误的例子如下：
1. 5天收益率，每天都产生信号。相当于有5份资金，每天都入了1份并持有了5天

问题：如果想计算因子持有期是1天、5天、10天收益更好，怎么处理？
1. 因子重采样成1天，5天，10天。然后相乘
    不同入场时间对结果有很大影响，时间长影响大。比如月度调仓抢跑
    不同周期的曲线不能画在同一图上
    不同周期的终值可以画在同一图上
2. 因子每天都入场，然后乘以1天、5天、10天的收益率。
    1. 相当于资金多了N份
    2. 每个收益都错开了一段，时间不同，不能直接相加。最后的总收益可以粗略相加N期求平均

"""
import numpy as np
import pandas as pd

from ta_cn.performance import weighted_index, ic, ir, ic_decay
from ta_cn.split import top_k, quantile_n

# 因子值
f = np.random.rand(10000000).reshape(-1, 5000)
# 持有1期收益
r = (np.random.rand(10000000).reshape(-1, 5000) - 0.5) / 100

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
