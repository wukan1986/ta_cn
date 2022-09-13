"""
公式转alpha191

国泰君安－基于短周期价量特征的多因子选股
"""

from ..imports import wide as W

CORR = W.ts_corr
REGSLOPE = W.LINEARREG_SLOPE
MEAN = W.SMA_TA
WMA = W.SMA_TA  # !!!WMA的公式没看懂，所以用另一个替代，以后再改
DECAYLINEAR = W.ts_decay_linear

CUMPROD = W.CUMPROD
FILTER = W.FILTER
RANK = W.rank
TSRANK = W.ts_rank
LessThan = W.less

IF = W.if_else
ABS = W.abs_
LOG = W.log  # 这里是用的自然对数
MAX = W.MAX2
MIN = W.MIN2
SIGN = W.sign

SMA = W.SMA_CN

COUNT = W.ts_count
DELTA = W.ts_delta
TSMAX = W.ts_max
HIGHDAY = W.ts_arg_max
TSMIN = W.ts_min
LOWDAY = W.ts_arg_min
MA = W.ts_mean
PROD = W.ts_product
DELAY = W.ts_delay
SUM = W.ts_sum
SUMIF = W.SUMIF  # 注意，SUMIF参数的位置常用的方式不同

REGBETA = W.SLOPE_YX_NB
REGRESI = W.REGRESI4

COVIANCE = W.ts_covariance
STD = W.ts_std_dev  # 引入的是全体标准差
