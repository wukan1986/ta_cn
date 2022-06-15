from .maths import *
from .over_bought_over_sold import *
from .pressure_support import *
from .reference import *
from .trend import *
from .volume import *

import talib as ta
TA_COMPATIBILITY_DEFAULT = 0  # 使用MA做第一个值
TA_COMPATIBILITY_METASTOCK = 1  # 使用Price做第一个值
# 非常关键的一步，有了它，EMA的计算方法就与国内一样了
# 但此句不要放在循环中使用，否则性能低下
ta.set_compatibility(TA_COMPATIBILITY_METASTOCK)
