"""
通达信公式转alpha191

国泰君安－基于短周期价量特征的多因子选股
"""
import numpy as np
import pandas as pd

import ta_cn.talib as ta

ta.init(mode=1, skipna=True)

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
from .utils import to_pd
from .utils_long import series_groupby_apply, dataframe_groupby_apply

"""
1. 将通达信公式改名成World Quant中对应公式
2. index用于groupby，将用于实现按股票分组计算滚动指标，按时间分组计算横截面
3. 逐元素指标用装饰器返回pandas
4. 按行和按列分组，都使用装饰器
"""


def FILTER(A, condition):
    return np.where(condition, A, 0)


def CUMPROD(A):
    return np.cumprod(A)


def REGRESI(y, *args, timeperiod=60):
    x = pd.concat(args, axis=1)
    coef, resi = ts_multiple_regress(y, x, timeperiod=timeperiod, add_constant=True)
    return resi


# 逐元素, 输出由numpy转pandas
IF = to_pd(IF)
LOG = to_pd(LOG)
SIGN = to_pd(SIGN)
MAX = to_pd(MAX)
MIN = to_pd(MIN)
ABS = to_pd(ABS)

# 按股票分组，计算时序指标。注意，组内时序需要已经排序
BY_ASSET = 'asset'
# 按时间分组。计算横截面
BY_DATE = 'date'
# 横截面上进行行业中性化
BY_GROUP = ['date', 'group']

dropna = False

# 时序
STD = series_groupby_apply(STD, by=BY_ASSET, to_kwargs=['timeperiod'])
HIGHDAY = series_groupby_apply(HIGHDAY, by=BY_ASSET, to_kwargs=['timeperiod'])
LOWDAY = series_groupby_apply(LOWDAY, by=BY_ASSET, to_kwargs=['timeperiod'])
DELTA = series_groupby_apply(DELTA, by=BY_ASSET, to_kwargs=['timeperiod'])
TSRANK = series_groupby_apply(TSRANK, by=BY_ASSET, to_kwargs=['timeperiod'])
DELAY = series_groupby_apply(DELAY, by=BY_ASSET, to_kwargs=['timeperiod'])
TSMAX = series_groupby_apply(TSMAX, by=BY_ASSET, to_kwargs=['timeperiod'])
TSMIN = series_groupby_apply(TSMIN, by=BY_ASSET, to_kwargs=['timeperiod'])
SUM = series_groupby_apply(SUM, by=BY_ASSET, to_kwargs=['timeperiod'])

DECAYLINEAR = series_groupby_apply(DECAYLINEAR, by=BY_ASSET, to_kwargs=['timeperiod'])
PROD = series_groupby_apply(PROD, by=BY_ASSET, to_kwargs=['timeperiod'])
MEAN = series_groupby_apply(MEAN, by=BY_ASSET, to_kwargs=['timeperiod'])
SMA = series_groupby_apply(SMA, by=BY_ASSET, to_kwargs=['timeperiod'])
COUNT = series_groupby_apply(COUNT, by=BY_ASSET, to_kwargs=['timeperiod'])
MA = series_groupby_apply(MA, by=BY_ASSET, to_kwargs=['timeperiod'])
WMA = series_groupby_apply(WMA, by=BY_ASSET, to_kwargs=['timeperiod'])
REGSLOPE = series_groupby_apply(REGSLOPE, by=BY_ASSET, to_kwargs=['timeperiod'])
CUMPROD = series_groupby_apply(CUMPROD, by=BY_ASSET, to_kwargs=[])

# 时序，双输入
CORR = dataframe_groupby_apply(CORR, by=BY_ASSET, dropna=True, to_df=[0, 1], to_kwargs={2: 'timeperiod'})
COVIANCE = dataframe_groupby_apply(COVIANCE, by=BY_ASSET, dropna=True, to_df=[0, 1], to_kwargs={2: 'timeperiod'})
REGBETA = dataframe_groupby_apply(REGBETA, by=BY_ASSET, dropna=dropna, to_df=[0, 1], to_kwargs={2: 'timeperiod'})

# 注意，SUMIF参数的位置常用的方式不同
SUMIF = dataframe_groupby_apply(SUMIF, by=BY_ASSET, dropna=dropna, to_df=[0, 1], to_kwargs={2: 'timeperiod'})
FILTER = dataframe_groupby_apply(FILTER, by=BY_ASSET, dropna=dropna, to_df=[0, 1], to_kwargs={})
REGRESI = dataframe_groupby_apply(REGRESI, by=BY_ASSET, dropna=dropna, to_df=[0, 1, 2, 3], to_kwargs={4: 'timeperiod'})

# 截面
RANK = series_groupby_apply(RANK, by=BY_DATE)

# 防止被IDE删除
LessThan = LessThan
