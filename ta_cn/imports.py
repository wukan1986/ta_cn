"""
导入公式清单

公式分布在多个文件，分别导入工作量大，所以直接导入本文件即可

以后遇到支持开拓者、文华一类的公式语言时，只要import as 做好映射即可
"""
from .ema import *
from .logical import *
from .maths import *
from .over_bought_over_sold import *
from .pressure_support import *
from .reference import *
from .statistics import *
from .ta import *
from .trend import *
from .volume import *

# from .slow import * # 计算慢的公式，可以找到替代

# 以下只是为了IDE代码格式化时不删除import
try:
    KDJ
    BOLL
    VR
    VARP
    TRIX
    BETWEEN
    ROUND
    DMA
    LLVBARS
    TA_SET_COMPATIBILITY_ENABLE
    # CCI
except:
    pass
