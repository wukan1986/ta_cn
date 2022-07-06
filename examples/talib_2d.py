import numpy as np

# 新版talib,只要替换引用，并添加一句init即可
import ta_cn.talib as ta
from ta_cn.utils import pushna, pullna

# 原版talib,不支持二维数据
# import talib as ta

# 准备数据
h = np.random.rand(1000000).reshape(-1, 5000) + 10
l = np.random.rand(1000000).reshape(-1, 5000)
c = np.random.rand(1000000).reshape(-1, 5000)
# 指定模式，否则对talib封装的所有函数都不存在
ta.init(mode=1, skipna=False)

# 几个调用函数演示
r = ta.ATR(h, l, c, timeperiod=10)
print(r)
x, y, z = ta.BBANDS(c, timeperiod=10, nbdevup=2, nbdevdn=2)
print(z)

# 将少量值设置为空，用来模拟停牌
c[c < 0.4] = np.nan

# 提前处理数据，跳过停牌进行计算，再还原的演示
# 嵌套指标时，全为时序指标使用down,或全为截面使用right。混合时此方法不要轻易使用
arr, row, col = pushna(c, direction='down')
rr = ta.SMA(arr, timeperiod=10)
r = pullna(rr, row, col)
print(r)

# 使用skip_na在内部跳过停牌
ta.init(mode=1, skipna=True)
r = ta.SMA(c, timeperiod=10)
print(r)

# 使用多参数
ta.init(mode=2, skipna=True)
r = ta.SMA(c, timeperiod=[10, 20])
print(r)
