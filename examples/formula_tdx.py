import numpy as np

# ta_cn.talib库底层是循环调用talib，部分计算效率不高
# 可导入ta_cn中的公式，只加这一句即导入多个文件中的函数
from ta_cn.imports import *
# 准备数据
from ta_cn.talib import init, set_compatibility_enable, set_compatibility

h = np.random.rand(10000000).reshape(-1, 50000) + 10
l = np.random.rand(10000000).reshape(-1, 50000)
c = np.random.rand(10000000).reshape(-1, 50000)

init(mode=2, skipna=False)

r = ATR_CN(h, l, c, timeperiod=10)
print(r)

# 设置参数，让MACD中的EMA算法与国内算法相同
set_compatibility_enable(True)
set_compatibility(1)
set_compatibility_enable(False)

x, y, z = MACD(c)
print(z)

"""
三种不同调用MACD的方法：

from ta_cn.imports import *
%timeit MACD(c)
499 ms ± 10 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

from ta_cn.slow import MACD_CN
%timeit MACD_CN(c)
3.59 s ± 58.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

import ta_cn.talib as ta
%timeit ta.MACD(c)
426 ms ± 1.46 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
"""
