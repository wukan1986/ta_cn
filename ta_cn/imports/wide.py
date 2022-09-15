"""
对指标的算子化包装
1. 包装成只支持 宽表 输入，输出是特殊格式，需要处理得到输出
2. 简化参数输入，命名参数也可当成位置参数输入
3. 通过堆叠的方法，自动跳过停牌

!!!函数太多，又想要智能提示，只能手工按需补充
"""
from .long import indneutralize
from .. import talib as ta
from ..alphas.alpha import CUMPROD
from ..alphas.alpha import FILTER_191
from ..ema import SMA_CN
from ..regress import REGRESI
from ..regress import SLOPE_YX
from ..tdx.reference import FILTER as FILTER_TDX
from ..tdx.reference import SUMIF
from ..utils_wide import wide_wraps, long_wraps
from ..wq.arithmetic import abs_
from ..wq.arithmetic import log
from ..wq.arithmetic import max_
from ..wq.arithmetic import min_
from ..wq.arithmetic import sign
from ..wq.arithmetic import signed_power
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

# 二维TALIB
_ta2d = ta.init(mode=2, skipna=False, to_globals=False)

# TALIB, 多输入
CORREL = wide_wraps(_ta2d.CORREL, input_num=2, to_kwargs={2: 'timeperiod'})
ATR = wide_wraps(_ta2d.ATR, input_num=3, to_kwargs={3: 'timeperiod'})

# TALIB, 单输入
LINEARREG_SLOPE = wide_wraps(_ta2d.LINEARREG_SLOPE)
SMA_TA = wide_wraps(_ta2d.SMA)
WMA = wide_wraps(_ta2d.WMA)

# WorldQuant，时序
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

# WorldQuant，横截面
rank = wide_wraps(rank, direction=None, to_kwargs={})
scale = wide_wraps(scale, direction=None, to_kwargs={1: 'scale'})

# WorldQuant
less = wide_wraps(less, input_num=2, to_kwargs={})
signed_power = wide_wraps(signed_power, direction=None, input_num=2, to_kwargs={})
if_else = wide_wraps(if_else, direction=None, input_num=3, to_kwargs={})
abs_ = wide_wraps(abs_, direction=None, to_kwargs={})
log = wide_wraps(log, direction=None, to_kwargs={})
max_ = wide_wraps(max_, direction=None, input_num=2, to_kwargs={})
min_ = wide_wraps(min_, direction=None, input_num=2, to_kwargs={})
sign = wide_wraps(sign, direction=None, to_kwargs={})

#
CUMPROD = wide_wraps(CUMPROD, to_kwargs={})
FILTER_191 = wide_wraps(FILTER_191, input_num=2, to_kwargs={})
FILTER_TDX = wide_wraps(FILTER_TDX, input_num=2, to_kwargs={1: 'N'})

#
SMA_CN = wide_wraps(SMA_CN, to_kwargs={1: 'timeperiod', 2: 'M'})

# 通达信导入
SUMIF = wide_wraps(SUMIF, input_num=2, to_kwargs={2: 'timeperiod'})

SLOPE_YX = wide_wraps(SLOPE_YX, input_num=2, to_kwargs={2: 'timeperiod'})
REGRESI4 = wide_wraps(REGRESI, input_num=4, to_kwargs={4: 'timeperiod'})

# 长表转宽表
# 行业中性化
indneutralize = long_wraps(indneutralize, direction='right')
