"""
对指标的算子化包装
1. 包装成只支持 长表 输入和输出
2. 简化参数输入，命名参数也可当成位置参数输入
3. 通过dropna的方法，自动跳过停牌

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
from ..aggregate import A_div_AB
from ..alpha import CUMPROD
from ..alpha import FILTER
from ..alpha import LessThan
from ..alpha import RANK
from ..alpha import TS_RANK
from ..alpha import scale
from ..ema import SMA
from ..preprocess import demean
from ..regress import REGRESI
from ..regress import SLOPE_YX_NB
from ..statistics import COVAR
from ..statistics import STDP
from ..utils import to_pd
from ..utils_long import dataframe_groupby_apply, series_groupby_apply

_ta1d = ta.init(mode=1, skipna=False, to_globals=False)

# 按股票分组，计算时序指标。注意，组内时序需要已经排序
BY_ASSET = 'asset'
# 按时间分组。计算横截面
BY_DATE = 'date'
# 横截面上进行行业中性化
BY_GROUP = ['date', 'group']

## TALIB, 多输入
CORREL = dataframe_groupby_apply(_ta1d.CORREL, by=BY_ASSET)
ATR = dataframe_groupby_apply(_ta1d.ATR, by=BY_ASSET, to_df=[0, 1, 2], to_kwargs={3: 'timeperiod'})

## TALIB, 单输入
LINEARREG_SLOPE = series_groupby_apply(_ta1d.LINEARREG_SLOPE, by=BY_ASSET)
SMA_TA = series_groupby_apply(_ta1d.SMA, by=BY_ASSET)
WMA = series_groupby_apply(_ta1d.WMA, by=BY_ASSET)

#
CUMPROD = series_groupby_apply(CUMPROD, by=BY_ASSET, to_kwargs={})
FILTER = dataframe_groupby_apply(FILTER, by=BY_ASSET, to_kwargs={}, dropna=False)
RANK = series_groupby_apply(RANK, by=BY_DATE, to_kwargs={})
TS_RANK = series_groupby_apply(TS_RANK, by=BY_ASSET)
LessThan = to_pd(LessThan)
scale = series_groupby_apply(scale, by=BY_DATE, to_kwargs={1: 'a'}, dropna=False)
signed_power = to_pd(signed_power)

#
if_else = to_pd(if_else)
abs = to_pd(abs)
log = to_pd(log)
MAX2 = to_pd(MAX)
MIN2 = to_pd(MIN)
sign = to_pd(sign)

#
SMA = series_groupby_apply(SMA, by=BY_ASSET, to_kwargs={1: 'timeperiod', 2: 'M'})

#
COUNT = series_groupby_apply(COUNT, by=BY_ASSET)
ts_delta = series_groupby_apply(ts_delta, by=BY_ASSET, to_kwargs={1: 'd'})
ts_max = series_groupby_apply(ts_max, by=BY_ASSET, to_kwargs={1: 'd'})
ts_arg_max = series_groupby_apply(ts_arg_max, by=BY_ASSET, to_kwargs={1: 'd'})
ts_min = series_groupby_apply(ts_min, by=BY_ASSET, to_kwargs={1: 'd'})
ts_arg_min = series_groupby_apply(ts_arg_min, by=BY_ASSET, to_kwargs={1: 'd'})
ts_mean = series_groupby_apply(ts_mean, by=BY_ASSET, to_kwargs={1: 'd'})
ts_product = series_groupby_apply(ts_product, by=BY_ASSET, to_kwargs={1: 'd'}, dropna=False)
ts_delay = series_groupby_apply(ts_delay, by=BY_ASSET, to_kwargs={1: 'd'})
ts_sum = series_groupby_apply(ts_sum, by=BY_ASSET, to_kwargs={1: 'd'})
SUMIF = dataframe_groupby_apply(SUMIF, by=BY_ASSET)

SLOPE_YX_NB = dataframe_groupby_apply(SLOPE_YX_NB, by=BY_ASSET)
REGRESI4 = dataframe_groupby_apply(REGRESI, by=BY_ASSET, to_df=[0, 1, 2, 3], to_kwargs={4: 'timeperiod'})

COVAR = dataframe_groupby_apply(COVAR, by=BY_ASSET)
STDP = series_groupby_apply(STDP, by=BY_ASSET)

# 行业中性。demean法
indneutralize = dataframe_groupby_apply(demean, by=BY_GROUP, to_df=[0, 'group'], to_kwargs={})

# 可用于 全部市场宽度
A_div_AB_1 = series_groupby_apply(A_div_AB, by=BY_DATE, to_kwargs={})
# 可用于 板块市场宽度
A_div_AB_2 = dataframe_groupby_apply(A_div_AB, by=BY_GROUP, to_df=[0, 'group'], to_kwargs={})
