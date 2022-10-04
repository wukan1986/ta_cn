"""
通达信公式，长表模式，跳过空值
"""
from .. import BY_ASSET
from ..ema import SMA_CN
from ..tdx.logical import BETWEEN
from ..tdx.logical import CROSS
from ..tdx.logical import EVERY
from ..tdx.logical import EXIST
from ..tdx.logical import LAST
from ..tdx.logical import VALUEWHEN
from ..tdx.over_bought_over_sold import ATR_CN
from ..tdx.over_bought_over_sold import BIAS
from ..tdx.over_bought_over_sold import KDJ
from ..tdx.over_bought_over_sold import MEDPRICE
from ..tdx.over_bought_over_sold import ROC
from ..tdx.over_bought_over_sold import RSI
from ..tdx.over_bought_over_sold import TYPPRICE
from ..tdx.over_bought_over_sold import WR
from ..tdx.pressure_support import BOLL
from ..tdx.reference import BARSLAST
from ..tdx.reference import BARSLASTCOUNT
from ..tdx.reference import BARSSINCEN
from ..tdx.reference import CONST
from ..tdx.reference import FILTER
from ..tdx.reference import SUMIF
from ..tdx.reference import TR
from ..tdx.statistics import AVEDEV
from ..tdx.statistics import STD
from ..tdx.statistics import STDP
from ..tdx.statistics import VAR
from ..tdx.statistics import VARP
from ..tdx.trend import BBI
from ..tdx.trend import DI
from ..tdx.trend import DM
from ..tdx.trend import DMI
from ..tdx.trend import DPO
from ..tdx.trend import MACD
from ..tdx.trend import MTM
from ..tdx.trend import PSY
from ..tdx.trend import TRIX
from ..tdx.volume import OBV
from ..tdx.volume import VR
from ..utils_long import dataframe_groupby_apply, series_groupby_apply

# 逻辑函数
CROSS = dataframe_groupby_apply(CROSS, by=BY_ASSET, to_kwargs={})
EVERY = series_groupby_apply(EVERY, by=BY_ASSET)
EXIST = series_groupby_apply(EXIST, by=BY_ASSET)
BETWEEN = dataframe_groupby_apply(BETWEEN, by=BY_ASSET, to_df=[0, 1, 2], to_kwargs={})
VALUEWHEN = dataframe_groupby_apply(VALUEWHEN, by=BY_ASSET, to_df=[0, 1], to_kwargs={})
LAST = series_groupby_apply(LAST, by=BY_ASSET, to_kwargs={1: 'n', 2: 'm'})

# 超买超卖
ATR_CN = dataframe_groupby_apply(ATR_CN, by=BY_ASSET, to_df=[0, 1, 2], to_kwargs={3: 'timeperiod'})
BIAS = series_groupby_apply(BIAS, by=BY_ASSET)
KDJ = dataframe_groupby_apply(KDJ, by=BY_ASSET, to_df=[0, 1, 2],
                              to_kwargs={3: 'fastk_period', 4: 'M1', 5: 'M2'}, output_num=3)
ROC = series_groupby_apply(ROC, by=BY_ASSET)
TYPPRICE = dataframe_groupby_apply(TYPPRICE, by=BY_ASSET, to_df=[0, 1, 2], to_kwargs={})
MEDPRICE = dataframe_groupby_apply(MEDPRICE, by=BY_ASSET, to_df=[0, 1], to_kwargs={})
WR = dataframe_groupby_apply(WR, by=BY_ASSET, to_df=[0, 1, 2], to_kwargs={3: 'timeperiod'})
RSI = series_groupby_apply(RSI, by=BY_ASSET)

# 压力支撑
BOLL = series_groupby_apply(BOLL, by=BY_ASSET, to_kwargs={1: 'timeperiod', 2: 'nbdevup', 3: 'nbdevdn'}, output_num=3)

# 引用
CONST = series_groupby_apply(CONST, by=BY_ASSET, to_kwargs={})
SUMIF = dataframe_groupby_apply(SUMIF, by=BY_ASSET, to_df=[0, 1], to_kwargs={2: 'timeperiod'})
TR = dataframe_groupby_apply(TR, by=BY_ASSET, to_df=[0, 1, 2], to_kwargs={})
FILTER = series_groupby_apply(FILTER, by=BY_ASSET, to_kwargs={1: 'N'})
BARSLAST = series_groupby_apply(BARSLAST, by=BY_ASSET, to_kwargs={})
BARSLASTCOUNT = series_groupby_apply(BARSLASTCOUNT, by=BY_ASSET, to_kwargs={})
BARSSINCEN = series_groupby_apply(BARSSINCEN, by=BY_ASSET)

# 统计
AVEDEV = series_groupby_apply(AVEDEV, by=BY_ASSET)
STD = series_groupby_apply(STD, by=BY_ASSET, to_kwargs={1: 'd'})
STDP = series_groupby_apply(STDP, by=BY_ASSET, to_kwargs={1: 'd'})
VAR = series_groupby_apply(VAR, by=BY_ASSET, to_kwargs={1: 'd'})
VARP = series_groupby_apply(VARP, by=BY_ASSET, to_kwargs={1: 'd'})

# 趋势
BBI = series_groupby_apply(BBI, by=BY_ASSET,
                           to_kwargs={1: 'timeperiod1', 2: 'timeperiod2', 3: 'timeperiod3', 4: 'timeperiod4'})
DPO = series_groupby_apply(DPO, by=BY_ASSET)
MACD = series_groupby_apply(MACD, by=BY_ASSET, to_kwargs={1: 'fastperiod', 2: 'slowperiod', 3: 'signalperiod'},
                            output_num=3)
MTM = series_groupby_apply(MTM, by=BY_ASSET)
PSY = series_groupby_apply(PSY, by=BY_ASSET)
DM = dataframe_groupby_apply(DM, by=BY_ASSET, to_df=[0, 1], to_kwargs={2: 'timeperiod'}, output_num=2)
DI = dataframe_groupby_apply(DI, by=BY_ASSET, to_df=[0, 1, 2], to_kwargs={3: 'timeperiod'}, output_num=2)
DMI = dataframe_groupby_apply(DMI, by=BY_ASSET, to_df=[0, 1, 2], to_kwargs={3: 'timeperiod'}, output_num=2)
TRIX = series_groupby_apply(TRIX, by=BY_ASSET)

# 成交量
OBV = dataframe_groupby_apply(OBV, by=BY_ASSET, to_df=[0, 1], to_kwargs={2: 'scale'})
VR = dataframe_groupby_apply(VR, by=BY_ASSET, to_df=[0, 1], to_kwargs={2: 'timeperiod'})

# EMA系列
SMA_CN = series_groupby_apply(SMA_CN, by=BY_ASSET, to_kwargs={1: 'timeperiod', 2: 'M'})

# WQ已经定义过的公式，通达信中别名
from .long_wq import abs_ as ABS
from .long_wq import add as ADD
from .long_wq import divide as DIV
from .long_wq import log as LN  # 自然对数
from .long_wq import log10 as LOG  # 10为底的对数
from .long_wq import max_ as MAX
from .long_wq import mean as MEAN
from .long_wq import min_ as MIN
from .long_wq import multiply as MUL
from .long_wq import round_ as ROUND
from .long_wq import sign as SGN
from .long_wq import subtract as SUB
from .long_wq import if_else as IF
from .long_wq import ts_count as COUNT
from .long_wq import ts_delay as REF
from .long_wq import ts_delta as DIFF
from .long_wq import ts_max as HHV
from .long_wq import ts_mean as MA
from .long_wq import ts_min as LLV
from .long_wq import ts_sum as SUM
from .long_wq import rank as RANK

ABS
MAX
MIN
REF
HHV
MA
LLV
SUM
ADD
SUB
MUL
DIV
ROUND
MEAN
LN
LOG
SGN
DIFF
IF
COUNT
RANK
