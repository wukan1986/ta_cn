"""
WQ公式，宽表模式，跳过空值
"""
from .long_wq import group_neutralize
from ..utils_wide import wide_wraps, long_wraps
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
abs_ = wide_wraps(abs_, direction=None, to_kwargs={})
add = wide_wraps(add, direction=None, input_num=2, to_kwargs={})
ceiling = wide_wraps(ceiling, direction=None, to_kwargs={})
densify = wide_wraps(densify, direction=None, to_kwargs={})
divide = wide_wraps(divide, direction=None, input_num=2, to_kwargs={})
exp = wide_wraps(exp, direction=None, to_kwargs={})
floor = wide_wraps(floor, direction=None, to_kwargs={})
fraction = wide_wraps(fraction, direction=None, to_kwargs={})
inverse = wide_wraps(inverse, direction=None, to_kwargs={})
log = wide_wraps(log, direction=None, to_kwargs={})
log10 = wide_wraps(log10, direction=None, to_kwargs={})
log_diff = wide_wraps(log_diff, direction=None, to_kwargs={})
max_ = wide_wraps(max_, direction=None, input_num=2, to_kwargs={})
mean = wide_wraps(mean, direction=None, input_num=2, to_kwargs={})
min_ = wide_wraps(min_, direction=None, input_num=2, to_kwargs={})
multiply = wide_wraps(multiply, direction=None, input_num=2, to_kwargs={})
nan_mask = wide_wraps(nan_mask, direction=None, input_num=2, to_kwargs={})
nan_out = wide_wraps(nan_out, direction=None, to_kwargs={2: 'lower', 3: 'upper'})
power = wide_wraps(power, direction=None, input_num=2, to_kwargs={})
purify = wide_wraps(purify, direction=None, to_kwargs={})
replace = wide_wraps(replace, direction=None, to_kwargs={2: 'target', 3: 'dest'})
reverse = wide_wraps(reverse, direction=None, to_kwargs={})
round_ = wide_wraps(round_, direction=None, to_kwargs={})
round_down = wide_wraps(round_down, direction=None, to_kwargs={})
sign = wide_wraps(sign, direction=None, to_kwargs={})
signed_power = wide_wraps(signed_power, direction=None, input_num=2, to_kwargs={})
s_log_1p = wide_wraps(s_log_1p, direction=None, to_kwargs={})
sqrt = wide_wraps(sqrt, direction=None, to_kwargs={})
subtract = wide_wraps(subtract, direction=None, input_num=2, to_kwargs={})
to_nan = wide_wraps(to_nan, direction=None, to_kwargs={2: 'value', 3: 'reverse'})
densify = wide_wraps(densify, direction=None, to_kwargs={})
log10 = wide_wraps(log10, direction=None, to_kwargs={})
mean = wide_wraps(mean, direction=None, input_num=2, to_kwargs={})

# Vector Operators
# Logical Operators
less = wide_wraps(less, input_num=2, to_kwargs={})
if_else = wide_wraps(if_else, direction=None, input_num=3, to_kwargs={})

# Transformational Operators

# Cross Sectional Operators
rank = wide_wraps(rank, direction=None, to_kwargs={})
scale = wide_wraps(scale, direction=None, to_kwargs={1: 'scale'})

# Group Operators
group_neutralize = long_wraps(group_neutralize, direction='right')

# Time Series Operators
ts_arg_max = wide_wraps(ts_arg_max, to_kwargs={1: 'd'})
ts_arg_min = wide_wraps(ts_arg_min, to_kwargs={1: 'd'})
ts_corr = wide_wraps(ts_corr, input_num=2, to_kwargs={2: 'd'})
ts_count = wide_wraps(ts_count, to_kwargs={1: 'd'})
ts_covariance = wide_wraps(ts_covariance, input_num=2, to_kwargs={2: 'd'})
ts_decay_linear = wide_wraps(ts_decay_linear, to_kwargs={1: 'd'})
ts_delay = wide_wraps(ts_delay, to_kwargs={1: 'd'})
ts_delta = wide_wraps(ts_delta, to_kwargs={1: 'd'})
ts_max = wide_wraps(ts_max, to_kwargs={1: 'd'})
ts_mean = wide_wraps(ts_mean, to_kwargs={1: 'd'})
ts_min = wide_wraps(ts_min, to_kwargs={1: 'd'})
ts_product = wide_wraps(ts_product, to_kwargs={1: 'd'})
ts_rank = wide_wraps(ts_rank, to_kwargs={1: 'd'})
ts_std_dev = wide_wraps(ts_std_dev, to_kwargs={1: 'd'})
ts_sum = wide_wraps(ts_sum, to_kwargs={1: 'd'})

# Special Operators
