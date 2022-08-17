"""
对指标的算子化包装
1. 包装成只支持 长表 输入和输出
2. 简化参数输入，命名参数也可当成位置参数输入
3. 通过dropna的方法，自动跳过停牌

!!!函数太多，又想要智能提示，只能手工按需补充
"""
import ta_cn.talib as ta
from ..alpha import CUMPROD
from ..alpha import FILTER
from ..alpha import LessThan
from ..alpha import RANK
from ..alpha import TS_RANK
from ..ema import SMA
from ..logical import IF
from ..maths import ABS
from ..maths import LN
from ..maths import MAX
from ..maths import MIN
from ..maths import SGN
from ..preprocess import demean
from ..reference import COUNT
from ..reference import DIFF
from ..reference import HHV
from ..reference import HHVBARS
from ..reference import LLV
from ..reference import LLVBARS
from ..reference import MA
from ..reference import PRODUCT
from ..reference import REF
from ..reference import SUM
from ..reference import SUMIF
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

#
IF = to_pd(IF)
ABS = to_pd(ABS)
LN = to_pd(LN)
MAX2 = to_pd(MAX)
MIN2 = to_pd(MIN)
SGN = to_pd(SGN)

#
SMA = series_groupby_apply(SMA, by=BY_ASSET, to_kwargs={1: 'timeperiod', 2: 'M'})

#
COUNT = series_groupby_apply(COUNT, by=BY_ASSET)
DIFF = series_groupby_apply(DIFF, by=BY_ASSET)
HHV = series_groupby_apply(HHV, by=BY_ASSET)
HHVBARS = series_groupby_apply(HHVBARS, by=BY_ASSET)
LLV = series_groupby_apply(LLV, by=BY_ASSET)
LLVBARS = series_groupby_apply(LLVBARS, by=BY_ASSET)
MA = series_groupby_apply(MA, by=BY_ASSET)
PRODUCT = series_groupby_apply(PRODUCT, by=BY_ASSET)
REF = series_groupby_apply(REF, by=BY_ASSET)
SUM = series_groupby_apply(SUM, by=BY_ASSET)
SUMIF = dataframe_groupby_apply(SUMIF, by=BY_ASSET)

SLOPE_YX_NB = dataframe_groupby_apply(SLOPE_YX_NB, by=BY_ASSET)
REGRESI4 = dataframe_groupby_apply(REGRESI, by=BY_ASSET, to_df=[0, 1, 2, 3], to_kwargs={4: 'timeperiod'})

COVAR = dataframe_groupby_apply(COVAR, by=BY_ASSET)
STDP = series_groupby_apply(STDP, by=BY_ASSET)

# 行业中性。demean法
indneutralize = dataframe_groupby_apply(demean, by=BY_GROUP, to_df=[0, 'group'], to_kwargs={})
