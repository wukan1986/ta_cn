"""
公式转alpha191

国泰君安－基于短周期价量特征的多因子选股
"""

from ..imports import long as L

CORR = L.ts_corr
REGSLOPE = L.LINEARREG_SLOPE
MEAN = L.SMA_TA
WMA = L.SMA_TA  # !!!WMA的公式没看懂，所以用另一个替代，以后再改
DECAYLINEAR = L.ts_decay_linear

CUMPROD = L.CUMPROD
FILTER = L.FILTER
RANK = L.rank
TSRANK = L.ts_rank
LessThan = L.less

IF = L.if_else
ABS = L.abs_
LOG = L.log  # 这里是用的自然对数
MAX = L.MAX2
MIN = L.MIN2
SIGN = L.sign

SMA = L.SMA_CN

COUNT = L.ts_count
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

REGBETA = L.SLOPE_YX
REGRESI = L.REGRESI4

COVIANCE = L.ts_covariance
STD = L.ts_std_dev  # 引入的是全体标准差
