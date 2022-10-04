"""
公式转alpha191

国泰君安－基于短周期价量特征的多因子选股
"""

from ..imports import long as L
from ..imports import long_ta as L_TA
from ..imports import long_tdx as L_TDX
from ..imports import long_wq as L_WQ

CORR = L_WQ.ts_corr
REGSLOPE = L_TA.LINEARREG_SLOPE
MEAN = L_TA.SMA
WMA = L_TA.SMA  # !!!WMA的公式没看懂，所以用另一个替代，以后再改
DECAYLINEAR = L_WQ.ts_decay_linear

CUMPROD = L.CUMPROD
FILTER = L.FILTER_191
RANK = L_WQ.rank
TSRANK = L_WQ.ts_rank
LessThan = L_WQ.less

IF = L_WQ.if_else
ABS = L_WQ.abs_
LOG = L_WQ.log  # 这里是用的自然对数
MAX = L_WQ.max_
MIN = L_WQ.min_
SIGN = L_WQ.sign

SMA = L_TDX.SMA_CN

COUNT = L_WQ.ts_count
DELTA = L_WQ.ts_delta
TSMAX = L_WQ.ts_max
HIGHDAY = L_WQ.ts_arg_max
TSMIN = L_WQ.ts_min
LOWDAY = L_WQ.ts_arg_min
MA = L_WQ.ts_mean
PROD = L_WQ.ts_product
DELAY = L_WQ.ts_delay
SUM = L_WQ.ts_sum
SUMIF = L_TDX.SUMIF  # 注意，SUMIF参数的位置常用的方式不同

REGBETA = L.SLOPE_YX
REGRESI = L.REGRESI4

COVIANCE = L_WQ.ts_covariance
STD = L_WQ.ts_std_dev  # 引入的是全体标准差
