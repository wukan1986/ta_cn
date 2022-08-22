"""
对指标的算子化包装
1. 包装成只支持 宽表 输入，输出是特殊格式，需要处理得到输出
2. 简化参数输入，命名参数也可当成位置参数输入
3. 通过堆叠的方法，自动跳过停牌

!!!函数太多，又想要智能提示，只能手工按需补充
"""
from .. import talib as ta
from ..alpha import CUMPROD
from ..alpha import FILTER
from ..alpha import LessThan
from ..alpha import RANK
from ..alpha import TS_RANK
from ..alpha import scale
from ..alpha import signedpower
from ..ema import SMA
from ..logical import IF
from ..maths import ABS
from ..maths import LN
from ..maths import MAX
from ..maths import MIN
from ..maths import SGN
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
signedpower = wide_wraps(signedpower, direction=None, input_num=2, to_kwargs={})  # 输入n不是数字，而是矩阵

#
IF = wide_wraps(IF, direction=None, input_num=3, to_kwargs={})
ABS = wide_wraps(ABS, direction=None, to_kwargs={})
LN = wide_wraps(LN, direction=None, to_kwargs={})
MAX2 = wide_wraps(MAX, direction=None, input_num=2, to_kwargs={})
MIN2 = wide_wraps(MIN, direction=None, input_num=2, to_kwargs={})
SGN = wide_wraps(SGN, direction=None, to_kwargs={})

#
SMA = wide_wraps(SMA, to_kwargs={1: 'timeperiod', 2: 'M'})

#
COUNT = wide_wraps(COUNT)
DIFF = wide_wraps(DIFF)
HHV = wide_wraps(HHV)
HHVBARS = wide_wraps(HHVBARS)
LLV = wide_wraps(LLV)
LLVBARS = wide_wraps(LLVBARS)
MA = wide_wraps(MA)
PRODUCT = wide_wraps(PRODUCT)
REF = wide_wraps(REF)
SUM = wide_wraps(SUM)
SUMIF = wide_wraps(SUMIF, input_num=2, to_kwargs={2: 'timeperiod'})

SLOPE_YX_NB = wide_wraps(SLOPE_YX_NB, input_num=2, to_kwargs={2: 'timeperiod'})
REGRESI4 = wide_wraps(REGRESI, input_num=4, to_kwargs={4: 'timeperiod'})

COVAR = wide_wraps(COVAR, input_num=2, to_kwargs={2: 'timeperiod'})
STDP = wide_wraps(STDP)

from .wide_long import indneutralize

indneutralize = indneutralize
