"""
对指标的算子化包装
1. 包装成只支持 宽表 输入，输出是特殊格式，需要处理得到输出
2. 简化参数输入，命名参数也可当成位置参数输入
3. 通过堆叠的方法，自动跳过停牌

!!!函数太多，又想要智能提示，只能手工按需补充
"""
from ta_cn.tdx.maths import MAX
from ta_cn.tdx.maths import MIN
from ta_cn.tdx.reference import COUNT
from ta_cn.tdx.reference import SUMIF
from ta_cn.wq.arithmetic import abs
from ta_cn.wq.arithmetic import log
from ta_cn.wq.arithmetic import sign
from ta_cn.wq.arithmetic import signed_power
from ta_cn.wq.logical import if_else
from ta_cn.wq.time_series import ts_arg_max
from ta_cn.wq.time_series import ts_arg_min
from ta_cn.wq.time_series import ts_delay
from ta_cn.wq.time_series import ts_delta
from ta_cn.wq.time_series import ts_max
from ta_cn.wq.time_series import ts_mean
from ta_cn.wq.time_series import ts_min
from ta_cn.wq.time_series import ts_product
from ta_cn.wq.time_series import ts_sum
from .. import talib as ta
from ..alpha import CUMPROD
from ..alpha import FILTER
from ..alpha import LessThan
from ..alpha import RANK
from ..alpha import TS_RANK
from ..alpha import scale
from ..ema import SMA
from ..regress import REGRESI
from ..regress import SLOPE_YX_NB
from ..statistics import COVAR
from ..statistics import STDP
from ..utils_wide import wide_wraps

_ta2d = ta.init(mode=2, skipna=False, to_globals=False)

# TALIB, 多输入
CORREL = wide_wraps(_ta2d.CORREL, input_num=2, to_kwargs={2: 'timeperiod'})
ATR = wide_wraps(_ta2d.ATR, input_num=3, to_kwargs={3: 'timeperiod'})

# TALIB, 单输入
LINEARREG_SLOPE = wide_wraps(_ta2d.LINEARREG_SLOPE)
SMA_TA = wide_wraps(_ta2d.SMA)
WMA = wide_wraps(_ta2d.WMA)

#
CUMPROD = wide_wraps(CUMPROD, to_kwargs={})
FILTER = wide_wraps(FILTER, input_num=2, to_kwargs={})
RANK = wide_wraps(RANK, direction='left', to_kwargs={})
TS_RANK = wide_wraps(TS_RANK)
LessThan = wide_wraps(LessThan, input_num=2, to_kwargs={})
scale = wide_wraps(scale, direction=None, to_kwargs={1: 'a'})
signed_power = wide_wraps(signed_power, direction=None, input_num=2, to_kwargs={})  # 输入n不是数字，而是矩阵

#
if_else = wide_wraps(if_else, direction=None, input_num=3, to_kwargs={})
abs = wide_wraps(abs, direction=None, to_kwargs={})
log = wide_wraps(log, direction=None, to_kwargs={})
MAX2 = wide_wraps(MAX, direction=None, input_num=2, to_kwargs={})
MIN2 = wide_wraps(MIN, direction=None, input_num=2, to_kwargs={})
sign = wide_wraps(sign, direction=None, to_kwargs={})

#
SMA = wide_wraps(SMA, to_kwargs={1: 'timeperiod', 2: 'M'})

#
COUNT = wide_wraps(COUNT)
ts_delta = wide_wraps(ts_delta, to_kwargs={1: 'd'})
ts_max = wide_wraps(ts_max, to_kwargs={1: 'd'})
ts_arg_max = wide_wraps(ts_arg_max, to_kwargs={1: 'd'})
ts_min = wide_wraps(ts_min, to_kwargs={1: 'd'})
ts_arg_min = wide_wraps(ts_arg_min, to_kwargs={1: 'd'})
ts_mean = wide_wraps(ts_mean, to_kwargs={1: 'd'})
ts_product = wide_wraps(ts_product, to_kwargs={1: 'd'})
ts_delay = wide_wraps(ts_delay, to_kwargs={1: 'd'})
ts_sum = wide_wraps(ts_sum, to_kwargs={1: 'd'})
SUMIF = wide_wraps(SUMIF, input_num=2, to_kwargs={2: 'timeperiod'})

SLOPE_YX_NB = wide_wraps(SLOPE_YX_NB, input_num=2, to_kwargs={2: 'timeperiod'})
REGRESI4 = wide_wraps(REGRESI, input_num=4, to_kwargs={4: 'timeperiod'})

COVAR = wide_wraps(COVAR, input_num=2, to_kwargs={2: 'timeperiod'})
STDP = wide_wraps(STDP)

from .wide_long import indneutralize

indneutralize = indneutralize
