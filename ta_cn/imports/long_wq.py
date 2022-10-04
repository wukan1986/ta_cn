"""
WQ公式，长表模式，跳过空值
"""
from .. import BY_ASSET, BY_DATE
from ..utils import to_pd
from ..utils_long import series_groupby_apply, dataframe_groupby_apply
from ..wq.arithmetic import abs_
from ..wq.arithmetic import add
from ..wq.arithmetic import ceiling
from ..wq.arithmetic import densify
from ..wq.arithmetic import divide
from ..wq.arithmetic import exp
from ..wq.arithmetic import floor
from ..wq.arithmetic import fraction
from ..wq.arithmetic import inverse
from ..wq.arithmetic import log
from ..wq.arithmetic import log10
from ..wq.arithmetic import log_diff
from ..wq.arithmetic import max_
from ..wq.arithmetic import mean
from ..wq.arithmetic import min_
from ..wq.arithmetic import multiply
from ..wq.arithmetic import nan_mask
from ..wq.arithmetic import nan_out
from ..wq.arithmetic import power
from ..wq.arithmetic import purify
from ..wq.arithmetic import replace
from ..wq.arithmetic import reverse
from ..wq.arithmetic import round_
from ..wq.arithmetic import round_down
from ..wq.arithmetic import s_log_1p
from ..wq.arithmetic import sign
from ..wq.arithmetic import signed_power
from ..wq.arithmetic import sqrt
from ..wq.arithmetic import subtract
from ..wq.arithmetic import to_nan
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

# Arithmetic Operators
abs_ = to_pd(abs_)
add = to_pd(add)
ceiling = to_pd(ceiling)
divide = to_pd(divide)
exp = to_pd(exp)
floor = to_pd(floor)
fraction = to_pd(fraction)
inverse = to_pd(inverse)
log = to_pd(log)
log_diff = to_pd(log_diff)
max_ = to_pd(max_)
min_ = to_pd(min_)
multiply = to_pd(multiply)
nan_mask = to_pd(nan_mask)
nan_out = to_pd(nan_out)
power = to_pd(power)
purify = to_pd(purify)
replace = to_pd(replace)
reverse = to_pd(reverse)
round_ = to_pd(round_)
round_down = to_pd(round_down)
sign = to_pd(sign)
signed_power = to_pd(signed_power)
s_log_1p = to_pd(s_log_1p)
sqrt = to_pd(sqrt)
subtract = to_pd(subtract)
to_nan = to_pd(to_nan)
densify = to_pd(densify)
log10 = to_pd(log10)
mean = to_pd(mean)

# Vector Operators
# Logical Operators
less = to_pd(less)
if_else = to_pd(if_else)

# Transformational Operators

# Cross Sectional Operators
rank = series_groupby_apply(rank, by=BY_DATE, to_kwargs={})
scale = series_groupby_apply(scale, by=BY_DATE, to_kwargs={1: 'scale'}, dropna=False)

# Group Operators
group_neutralize = group_neutralize

# Time Series Operators
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

# Special Operators
