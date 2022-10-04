"""
公式转alpha191

国泰君安－基于短周期价量特征的多因子选股
"""
from ..imports import wide as W
from ..imports import wide_ta as W_TA
from ..imports import wide_tdx as W_TDX
from ..imports import wide_wq as W_WQ

CORR = W_WQ.ts_corr
REGSLOPE = W_TA.LINEARREG_SLOPE
MEAN = W_TA.SMA
WMA = W_TA.SMA  # !!!WMA的公式没看懂，所以用另一个替代，以后再改
DECAYLINEAR = W_WQ.ts_decay_linear

CUMPROD = W.CUMPROD
FILTER = W.FILTER_191
RANK = W_WQ.rank
TSRANK = W_WQ.ts_rank
LessThan = W_WQ.less

IF = W_WQ.if_else
ABS = W_WQ.abs_
LOG = W_WQ.log  # 这里是用的自然对数
MAX = W_WQ.max_
MIN = W_WQ.min_
SIGN = W_WQ.sign

SMA = W_TDX.SMA_CN

COUNT = W_WQ.ts_count
DELTA = W_WQ.ts_delta
TSMAX = W_WQ.ts_max
HIGHDAY = W_WQ.ts_arg_max
TSMIN = W_WQ.ts_min
LOWDAY = W_WQ.ts_arg_min
MA = W_WQ.ts_mean
PROD = W_WQ.ts_product
DELAY = W_WQ.ts_delay
SUM = W_WQ.ts_sum
SUMIF = W_TDX.SUMIF  # 注意，SUMIF参数的位置常用的方式不同

REGBETA = W.SLOPE_YX
REGRESI = W.REGRESI4

COVIANCE = W_WQ.ts_covariance
STD = W_WQ.ts_std_dev  # 引入的是全体标准差
