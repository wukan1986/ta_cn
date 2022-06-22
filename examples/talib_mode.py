import numpy as np

# 新版talib,只要替换引用即可直接支持二维数据
import ta_cn.talib as ta
from ta_cn.utils import pushna, pullna

# 原版talib,不支持二维数据
# import talib as ta

# 默认会启用模式1，这里设置成模式二
# 注意：周期等参数一定得使用命名参数，开高低收等一定要使用位置参数
ta.init(mode=2)

# 准备数据
h = np.random.rand(10000000).reshape(-1, 50000) + 10
l = np.random.rand(10000000).reshape(-1, 50000)
c = np.random.rand(10000000).reshape(-1, 50000)

# 几个调用函数演示
r = ta.ATR(h, l, c, timeperiod=[10, 20])
print(r)
x, y, z = ta.BBANDS(c, timeperiod=10, nbdevup=2, nbdevdn=2)
print(z)

# 将少量值设置为空，用来模拟停牌
c[c < 0.05] = np.nan
print(c)

# 跳过停牌进行计算，再还原的演示
arr, row, col = pushna(c, direction='down')
rr = ta.SMA(arr, timeperiod=10)
r = pullna(rr, row, col)
print(r)
