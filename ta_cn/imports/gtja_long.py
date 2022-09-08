"""
通达信公式转alpha191

国泰君安－基于短周期价量特征的多因子选股
"""

from ..imports import long as L

CORR = L.CORREL
REGSLOPE = L.LINEARREG_SLOPE
MEAN = L.SMA_TA
WMA = L.SMA_TA  # !!!WMA的公式没看懂，所以用另一个替代，以后再改
DECAYLINEAR = L.WMA

CUMPROD = L.CUMPROD
FILTER = L.FILTER
RANK = L.RANK
TSRANK = L.TS_RANK
LessThan = L.LessThan

IF = L.if_else
ABS = L.abs
LOG = L.log  # 这里是用的自然对数
MAX = L.MAX2
MIN = L.MIN2
SIGN = L.sign

SMA = L.SMA

COUNT = L.COUNT
DELTA = L.ts_delta
TSMAX = L.ts_max
HIGHDAY = L.ts_arg_max
TSMIN = L.ts_min
LOWDAY = L.ts_arg_min
MA = L.ts_mean
PROD = L.ts_product
DELAY = L.ts_delay
SUM = L.ts_sum
SUMIF = L.SUMIF  # 注意，SUMIF参数的位置常用的方式不同

REGBETA = L.SLOPE_YX_NB
REGRESI = L.REGRESI4

COVIANCE = L.COVAR
STD = L.STDP  # 引入的是全体标准差
