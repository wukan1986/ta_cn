"""
对指标的算子化包装
1. 包装成只支持 长表 输入和输出
2. 简化参数输入，命名参数也可当成位置参数输入
3. 通过dropna的方法，自动跳过停牌

!!!函数太多，又想要智能提示，只能手工按需补充
"""
from .. import talib as ta, BY_ASSET, BY_DATE, BY_GROUP
from ..aggregate import A_div_AB
from ..alphas.alpha import CUMPROD
from ..alphas.alpha import FILTER_191
from ..ema import SMA_CN
from ..regress import REGRESI
from ..regress import SLOPE_YX
from ..tdx.logical import CROSS
from ..tdx.reference import FILTER as FILTER_TDX
from ..tdx.reference import SUMIF
from ..utils import to_pd
from ..utils_long import dataframe_groupby_apply, series_groupby_apply
from ..wq.arithmetic import abs_
from ..wq.arithmetic import log
from ..wq.arithmetic import max_
from ..wq.arithmetic import min_
from ..wq.arithmetic import sign
from ..wq.arithmetic import signed_power
from ..wq.cross_sectional import rank
from ..wq.cross_sectional import scale
from ..wq.group import group_neutralize
from ..wq.logical import if_else
from ..wq.logical import less
from ..wq.time_series import ts_arg_max
from ..wq.time_series import ts_arg_min
from ..wq.time_series import ts_corr
from ..wq.time_series import ts_count
from ..wq.time_series import ts_covariance
from ..wq.time_series import ts_decay_linear
from ..wq.time_series import ts_delay
from ..wq.time_series import ts_delta
from ..wq.time_series import ts_max
from ..wq.time_series import ts_mean
from ..wq.time_series import ts_min
from ..wq.time_series import ts_product
from ..wq.time_series import ts_rank
from ..wq.time_series import ts_std_dev
from ..wq.time_series import ts_sum

# 一维TALIB
_ta1d = ta.init(mode=1, skipna=False, to_globals=False)


## TALIB, 多输入
CORREL = dataframe_groupby_apply(_ta1d.CORREL, by=BY_ASSET)
ATR = dataframe_groupby_apply(_ta1d.ATR, by=BY_ASSET, to_df=[0, 1, 2], to_kwargs={3: 'timeperiod'})

## TALIB, 单输入
LINEARREG_SLOPE = series_groupby_apply(_ta1d.LINEARREG_SLOPE, by=BY_ASSET)
SMA_TA = series_groupby_apply(_ta1d.SMA, by=BY_ASSET)
WMA = series_groupby_apply(_ta1d.WMA, by=BY_ASSET)

# WorldQuant，时序
ts_arg_max = series_groupby_apply(ts_arg_max, by=BY_ASSET, to_kwargs={1: 'd'})
ts_arg_min = series_groupby_apply(ts_arg_min, by=BY_ASSET, to_kwargs={1: 'd'})
ts_corr = dataframe_groupby_apply(ts_corr, by=BY_ASSET, to_kwargs={2: 'd'})
ts_count = series_groupby_apply(ts_count, by=BY_ASSET, to_kwargs={1: 'd'})
ts_covariance = dataframe_groupby_apply(ts_covariance, by=BY_ASSET, to_kwargs={2: 'd'})
ts_decay_linear = series_groupby_apply(ts_decay_linear, by=BY_ASSET, to_kwargs={1: 'd'})
ts_delay = series_groupby_apply(ts_delay, by=BY_ASSET, to_kwargs={1: 'd'})
ts_delta = series_groupby_apply(ts_delta, by=BY_ASSET, to_kwargs={1: 'd'})
ts_max = series_groupby_apply(ts_max, by=BY_ASSET, to_kwargs={1: 'd'})
ts_mean = series_groupby_apply(ts_mean, by=BY_ASSET, to_kwargs={1: 'd'})
ts_min = series_groupby_apply(ts_min, by=BY_ASSET, to_kwargs={1: 'd'})
ts_product = series_groupby_apply(ts_product, by=BY_ASSET, to_kwargs={1: 'd'}, dropna=False)
ts_rank = series_groupby_apply(ts_rank, by=BY_ASSET, to_kwargs={1: 'd'})
ts_std_dev = series_groupby_apply(ts_std_dev, by=BY_ASSET, to_kwargs={1: 'd'})
ts_sum = series_groupby_apply(ts_sum, by=BY_ASSET, to_kwargs={1: 'd'})

# WorldQuant，横截面
rank = series_groupby_apply(rank, by=BY_DATE, to_kwargs={})
scale = series_groupby_apply(scale, by=BY_DATE, to_kwargs={1: 'scale'}, dropna=False)

# WorldQuant
less = to_pd(less)
signed_power = to_pd(signed_power)
if_else = to_pd(if_else)
abs_ = to_pd(abs_)
log = to_pd(log)
max_ = to_pd(max_)
min_ = to_pd(min_)
sign = to_pd(sign)

# 特殊
CUMPROD = series_groupby_apply(CUMPROD, by=BY_ASSET, to_kwargs={})
FILTER_191 = dataframe_groupby_apply(FILTER_191, by=BY_ASSET, to_kwargs={}, dropna=False)
FILTER_TDX = series_groupby_apply(FILTER_TDX, by=BY_ASSET, to_kwargs={1: 'N'})
#


#
SMA_CN = series_groupby_apply(SMA_CN, by=BY_ASSET, to_kwargs={1: 'timeperiod', 2: 'M'})

#

SUMIF = dataframe_groupby_apply(SUMIF, by=BY_ASSET)

SLOPE_YX = dataframe_groupby_apply(SLOPE_YX, by=BY_ASSET)
REGRESI4 = dataframe_groupby_apply(REGRESI, by=BY_ASSET, to_df=[0, 1, 2, 3], to_kwargs={4: 'timeperiod'})

# 行业中性
group_neutralize = group_neutralize

# 可用于 全部市场宽度
A_div_AB_1 = series_groupby_apply(A_div_AB, by=BY_DATE, to_kwargs={})
# 可用于 板块市场宽度
A_div_AB_2 = dataframe_groupby_apply(A_div_AB, by=BY_GROUP, to_df=[0, 'group'], to_kwargs={})

CROSS = dataframe_groupby_apply(CROSS, by=BY_ASSET, to_kwargs={})
