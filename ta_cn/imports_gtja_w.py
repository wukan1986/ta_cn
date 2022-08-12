"""
通达信公式转alpha191

国泰君安－基于短周期价量特征的多因子选股
"""
import numpy as np

import ta_cn.talib as ta
from .utils_wide import wide_wraps

ta.init(mode=2, skipna=True)

# 都是单支股票的循环，直接调用更快
from ta_cn.talib import CORREL as CORR
from ta_cn.talib import LINEARREG_SLOPE as REGSLOPE
from ta_cn.talib import SMA as MEAN
from ta_cn.talib import SMA as WMA  # !!!WMA的公式没看懂，所以用另一个替代，以后再改
from ta_cn.talib import WMA as DECAYLINEAR

from .alpha import LessThan
from .alpha import RANK
from .alpha import TS_RANK as TSRANK
from .ema import SMA
from .logical import IF
from .maths import ABS
from .maths import LN as LOG  # 引入的是自然对数
from .maths import MAX
from .maths import MIN
from .maths import SGN as SIGN
from .reference import COUNT
from .reference import DIFF as DELTA
from .reference import HHV as TSMAX
from .reference import HHVBARS as HIGHDAY
from .reference import LLV as TSMIN
from .reference import LLVBARS as LOWDAY
from .reference import MA
from .reference import PRODUCT as PROD
from .reference import REF as DELAY
from .reference import SUM
from .reference import SUMIF
from .regress import SLOPE_YX_NB as REGBETA
from .regress import ts_multiple_regress
from .statistics import COVAR as COVIANCE
from .statistics import STDP as STD  # 引入的是全体标准差
from .utils_long import dataframe_groupby_apply

"""
1. 将通达信公式改名成World Quant中对应公式
2. index用于groupby，将用于实现按股票分组计算滚动指标，按时间分组计算横截面
3. 逐元素指标用装饰器返回pandas
4. 按行和按列分组，都使用装饰器
"""


def FILTER(A, condition):
    return np.where(condition, A, 0)


def CUMPROD(A):
    if A.ndim == 2:
        return np.cumsum(A, axis=0)
    else:
        return np.cumprod(A)


def REGRESI(y, *args, timeperiod=60):
    x = np.concatenate(args, axis=1)
    coef, resi = ts_multiple_regress(y, x, timeperiod=timeperiod, add_constant=True)
    return resi


# 逐元素, 输出由numpy转pandas
IF = wide_wraps(IF, direction=None, input_num=3, output_num=1, to_kwargs={})
LOG = wide_wraps(LOG, direction=None, input_num=1, output_num=1, to_kwargs={})
SIGN = wide_wraps(SIGN, direction=None, input_num=1, output_num=1, to_kwargs={})
MAX = wide_wraps(MAX, direction=None, input_num=2, output_num=1, to_kwargs={})
MIN = wide_wraps(MIN, direction=None, input_num=2, output_num=1, to_kwargs={})
ABS = wide_wraps(ABS, direction=None, input_num=1, output_num=1, to_kwargs={})

# 按股票分组，计算时序指标。注意，组内时序需要已经排序
BY_ASSET = 'asset'
# 按时间分组。计算横截面
BY_DATE = 'date'
# 横截面上进行行业中性化
BY_GROUP = ['date', 'group']

dropna = False

# 时序
STD = wide_wraps(STD, direction='down', input_num=1, output_num=1, to_kwargs={1: 'timeperiod'})
HIGHDAY = wide_wraps(HIGHDAY, direction='down', input_num=1, output_num=1, to_kwargs={1: 'timeperiod'})
LOWDAY = wide_wraps(LOWDAY, direction='down', input_num=1, output_num=1, to_kwargs={1: 'timeperiod'})
DELTA = wide_wraps(DELTA, direction='down', input_num=1, output_num=1, to_kwargs={1: 'timeperiod'})
TSRANK = wide_wraps(TSRANK, direction='down', input_num=1, output_num=1, to_kwargs={1: 'timeperiod'})
DELAY = wide_wraps(DELAY, direction='down', input_num=1, output_num=1, to_kwargs={1: 'timeperiod'})
TSMAX = wide_wraps(TSMAX, direction='down', input_num=1, output_num=1, to_kwargs={1: 'timeperiod'})
TSMIN = wide_wraps(TSMIN, direction='down', input_num=1, output_num=1, to_kwargs={1: 'timeperiod'})
SUM = wide_wraps(SUM, direction='down', input_num=1, output_num=1, to_kwargs={1: 'timeperiod'})

DECAYLINEAR = wide_wraps(DECAYLINEAR, direction='down', input_num=1, output_num=1, to_kwargs={1: 'timeperiod'})
PROD = wide_wraps(PROD, direction='down', input_num=1, output_num=1, to_kwargs={1: 'timeperiod'})
MEAN = wide_wraps(MEAN, direction='down', input_num=1, output_num=1, to_kwargs={1: 'timeperiod'})
SMA = wide_wraps(SMA, direction='down', input_num=1, output_num=1, to_kwargs={1: 'timeperiod', 2: 'M'})
COUNT = wide_wraps(COUNT, direction='down', input_num=1, output_num=1, to_kwargs={1: 'timeperiod'})
MA = wide_wraps(MA, direction='down', input_num=1, output_num=1, to_kwargs={1: 'timeperiod'})
WMA = wide_wraps(WMA, direction='down', input_num=1, output_num=1, to_kwargs={1: 'timeperiod'})
REGSLOPE = wide_wraps(REGSLOPE, direction='down', input_num=1, output_num=1, to_kwargs={1: 'timeperiod'})
CUMPROD = wide_wraps(CUMPROD, direction='down', input_num=1, output_num=1, to_kwargs={})

# 时序，双输入
CORR = wide_wraps(CORR, direction='down', input_num=2, output_num=1, to_kwargs={2: 'timeperiod'})
COVIANCE = wide_wraps(COVIANCE, direction='down', input_num=2, output_num=1, to_kwargs={2: 'timeperiod'})
REGBETA = wide_wraps(REGBETA, direction='down', input_num=2, output_num=1, to_kwargs={2: 'timeperiod'})

# 注意，SUMIF参数的位置常用的方式不同
SUMIF = wide_wraps(SUMIF, direction='down', input_num=2, output_num=1, to_kwargs={2: 'timeperiod'})
FILTER = wide_wraps(FILTER, direction='down', input_num=2, output_num=1, to_kwargs={})
REGRESI = wide_wraps(REGRESI, direction='down', input_num=4, output_num=1, to_kwargs={4: 'timeperiod'})

# 截面
RANK = wide_wraps(RANK, direction='left', input_num=1, output_num=1)

# 防止被IDE删除
LessThan = LessThan
