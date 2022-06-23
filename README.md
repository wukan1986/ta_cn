# ta_cn 中国版技术指标

## 项目背景
初学量化，技术指标一般使用`TA-Lib`，但存在以下问题
1. 部分技术指标与国内不同。但大部分中国股民都是参考国内技术指标进行交易。需要实现中国版指标
2. `TA-Lib`只支持单支序列，要计算多支股票需循环，耗时久。

在实现遗传算法挖因子时，意识到如果能将常用的操作都转成算子，将大大简化策略的研究，
特别是将`+`、`-`、`*`、`/`等中缀操作符转成`ADD()`、`SUB()`、`MUL()`、`DIV()`前缀函数，可直接输到遗传算法工具中

所以开始参考`Alpha101`和各券商金融工程研报，试着实现一些算子，但后期实现中发现一些问题
1. 每家金工的研报指标命名上都有区别，难以统一
2. 指标太多，实现工作太大

直到看到了`MyTT`这个项目才意识到，指标命名参考股票软件的公式才是最方便直接的，可以直接到各股软中复制公式。遇到性能问题再针对性转换即可。

## 本人为何不直接用`MyTT`，而是重复超轮子呢？
1. 大部分公式只支持单条数据，遇到几千支股票的DataFrame，循环太慢
2. `TA-Lib`与国内指标不同，区别在哪，没有对比。错过了很好的教学机会
3. 为了行数短牺牲了可读性
4. 部分函数直接复制于股票软件，代码没有优化，有重复计算

## 目标
1. 按通达信等国内常用软件命名和分类各指标
2. 支持二维矩阵计算
3. 国内外计算方法区别很大时，两个版本都提供，同时说明区别处

## 实现方案优先级
1. bottleneck。支持二维数据，优先使用
2. TA-Lib。封装了常用函数，次要选择
3. numba。速度受影响，最后才用它

## 安装
1. 只想使用二维矩阵TA-Lib，只需安装基础版即可
```commandline
pip install ta_cn -i https://mirrors.aliyun.com/pypi/simple --upgrade
```

2. 使用全功能版，包括中国版指标加速
```commandline
pip install ta_cn[all] -i https://mirrors.aliyun.com/pypi/simple --upgrade
```

## TA-Lib由一维向量扩展到二维矩阵
使用了一些编程技巧，可以直接输入二维矩阵。需要注意的是：
1. TA-Lib遇到空值后面结果全为NaN
2. 停牌时，数据为NaN, 所以二维矩阵计算前需要特殊处理
3. 本人提供的方案是将数据压到最尾部，计算，然后还原

```python
import numpy as np

# 原版talib,不支持二维数据
# import talib as ta

# 新版talib,只要替换引用即可直接支持二维数据
import ta_cn.talib as ta
from ta_cn.utils import pushna, pullna

# 准备数据
h = np.random.rand(10000000).reshape(-1, 50000) + 10
l = np.random.rand(10000000).reshape(-1, 50000)
c = np.random.rand(10000000).reshape(-1, 50000)

# 几个调用函数演示
r = ta.ATR(h, l, c, 10)
print(r)
x, y, z = ta.BBANDS(c, timeperiod=10, nbdevup=2, nbdevdn=2)
print(z)

# 将少量值设置为空，用来模拟停牌
c[c < 0.05] = np.nan

# 跳过停牌进行计算，再还原的演示
arr, row, col = pushna(c, direction='down')
rr = ta.SMA(real=arr, timeperiod=10)
r = pullna(rr, row, col)
print(r)
```

还支持为不同列指定不同参数。例如：
```python
import ta_cn.talib as ta

ta.init(mode=2)
ta.SMA(arr, timeperiod=[10, 20, 30])

```

## 使用ta_cn中定义的公式
```python
import numpy as np

# ta_cn.talib库底层是循环调用talib，部分计算效率不高
# 可导入ta_cn中的公式，只加这一句即导入多个文件中的函数
from ta_cn.imports import *

# 准备数据
h = np.random.rand(10000000).reshape(-1, 50000) + 10
l = np.random.rand(10000000).reshape(-1, 50000)
c = np.random.rand(10000000).reshape(-1, 50000)

r = ATR_CN(h, l, c, timeperiod=10)
print(r)

# 设置参数，让MACD中的EMA算法与国内算法相同
TA_SET_COMPATIBILITY_ENABLE(True)
TA_SET_COMPATIBILITY(1) # 循环调用没有必要，所以放在前边
TA_SET_COMPATIBILITY_ENABLE(False)

x, y, z = MACD(c)
print(z)
```

## 输入DataFrame，输出是ndarray?
只要通过np_to_pd，并传入index/columns两参数即可还原成DataFrame
```python
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

```

## 指标对比清单
参考 [指标对比](指标对比.xlsx) 未完工，待补充

## 停牌处理2
1. 板块指数，停牌了也要最近的行情进行计算，否则指数过小
2. 停牌期的开高低收都是最近的收盘价，收盘价可以ffill

## 参考项目
1. [TA-Lib](https://github.com/TA-Lib/ta-lib) TA-Lib C语言版，非官方镜像
2. [ta-lib](https://github.com/mrjbq7/ta-lib) TA-Lib Python版封装
3. [MyTT](https://github.com/mpquant/MyTT) My麦语言 T通达信 T同花顺
4. [funcat](https://github.com/cedricporter/funcat) 公式移植
5. [pandas-ta](https://github.com/twopirllc/pandas-ta) 支持Pandas扩展的技术指标
6. [ta](https://github.com/bukosabino/ta) 通过类实现的技术指标

## 交流群
ta_cn技术指标交流群: 601477228