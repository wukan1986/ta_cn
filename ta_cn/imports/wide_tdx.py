"""
通达信公式，宽表模式，跳过空值
"""
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

from ..utils_wide import wide_wraps

# 逻辑函数
CROSS = wide_wraps(CROSS, input_num=2, to_kwargs={})
EVERY = wide_wraps(EVERY)
EXIST = wide_wraps(EXIST)
BETWEEN = wide_wraps(BETWEEN, input_num=3, to_kwargs={})
VALUEWHEN = wide_wraps(VALUEWHEN, input_num=2, to_kwargs={})
LAST = wide_wraps(LAST, to_kwargs={1: 'n', 2: 'm'})

# 超买超卖
ATR_CN = wide_wraps(ATR_CN, input_num=3, to_kwargs={3: 'timeperiod'})
BIAS = wide_wraps(BIAS)
KDJ = wide_wraps(KDJ, input_num=3, to_kwargs={3: 'fastk_period', 4: 'M1', 5: 'M2'}, output_num=3)
ROC = wide_wraps(ROC)
TYPPRICE = wide_wraps(TYPPRICE, input_num=3, to_kwargs={})
MEDPRICE = wide_wraps(MEDPRICE, input_num=2, to_kwargs={})
RSI = wide_wraps(RSI)

# 压力支撑
BOLL = wide_wraps(BOLL, to_kwargs={1: 'timeperiod', 2: 'nbdevup', 3: 'nbdevdn'}, output_num=3)

# 引用
CONST = wide_wraps(CONST, to_kwargs={})
SUMIF = wide_wraps(SUMIF, input_num=2, to_kwargs={2: 'timeperiod'})
TR = wide_wraps(TR, input_num=3, to_kwargs={})
FILTER = wide_wraps(FILTER, to_kwargs={1: 'N'})
BARSLAST = wide_wraps(BARSLAST, to_kwargs={})
BARSLASTCOUNT = wide_wraps(BARSLASTCOUNT, to_kwargs={})
BARSSINCEN = wide_wraps(BARSSINCEN)

# 统计
AVEDEV = wide_wraps(AVEDEV)
STD = wide_wraps(STD, to_kwargs={1: 'd'})
STDP = wide_wraps(STDP, to_kwargs={1: 'd'})
VAR = wide_wraps(VAR, to_kwargs={1: 'd'})
VARP = wide_wraps(VARP, to_kwargs={1: 'd'})

# 趋势
BBI = wide_wraps(BBI, to_kwargs={1: 'timeperiod1', 2: 'timeperiod2', 3: 'timeperiod3', 4: 'timeperiod4'})
DPO = wide_wraps(DPO)
MACD = wide_wraps(MACD, to_kwargs={1: 'fastperiod', 2: 'slowperiod', 3: 'signalperiod'}, output_num=3)
MTM = wide_wraps(MTM)
PSY = wide_wraps(PSY)
DM = wide_wraps(DM, input_num=2, to_kwargs={2: 'timeperiod'}, output_num=2)
DI = wide_wraps(DI, input_num=3, to_kwargs={3: 'timeperiod'}, output_num=2)
DMI = wide_wraps(DMI, input_num=3, to_kwargs={3: 'timeperiod'}, output_num=2)
TRIX = wide_wraps(TRIX)

# 成交量
OBV = wide_wraps(OBV, input_num=2, to_kwargs={2: 'scale'})
VR = wide_wraps(VR, input_num=2, to_kwargs={2: 'timeperiod'})

# EMA系列
SMA_CN = wide_wraps(SMA_CN, to_kwargs={1: 'timeperiod', 2: 'M'})

# WQ已经定义过的公式，通达信中别名
from .wide_wq import abs_ as ABS
from .wide_wq import add as ADD
from .wide_wq import divide as DIV
from .wide_wq import log as LN  # 自然对数
from .wide_wq import log10 as LOG  # 10为底的对数
from .wide_wq import max_ as MAX
from .wide_wq import mean as MEAN
from .wide_wq import min_ as MIN
from .wide_wq import multiply as MUL
from .wide_wq import round_ as ROUND
from .wide_wq import sign as SGN
from .wide_wq import subtract as SUB
from .wide_wq import if_else as IF
from .wide_wq import ts_count as COUNT
from .wide_wq import ts_delay as REF
from .wide_wq import ts_delta as DIFF
from .wide_wq import ts_max as HHV
from .wide_wq import ts_mean as MA
from .wide_wq import ts_min as LLV
from .wide_wq import ts_sum as SUM
from .wide_wq import rank as RANK

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
