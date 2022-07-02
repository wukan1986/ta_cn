"""
通达信公式转alpha101
"""

from talib import LINEARREG_SLOPE as REGBETA
from talib import SMA as MEAN

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
from .reference import WMA as DECAYLINEAR
from .statistics import CORREL as CORR
from .statistics import COVAR as COVIANCE
from .statistics import STDP as STD  # 引入的是全体标准差
from .utils import to_pd, series_groupby_apply, dataframe_groupby_apply

"""
1. 将通达信公式改名成World Quant中对应公式
2. index用于groupby，将用于实现按股票分组计算滚动指标，按时间分组计算横截面
3. 逐元素指标用装饰器返回pandas
4. 按行和按列分组，都使用装饰器
"""

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

# 时序
STD = series_groupby_apply(STD, by=BY_ASSET, dropna=False)
HIGHDAY = series_groupby_apply(HIGHDAY, by=BY_ASSET, dropna=False)
LOWDAY = series_groupby_apply(LOWDAY, by=BY_ASSET, dropna=False)
DELTA = series_groupby_apply(DELTA, by=BY_ASSET, dropna=False)
TSRANK = series_groupby_apply(TSRANK, by=BY_ASSET, dropna=False)
DELAY = series_groupby_apply(DELAY, by=BY_ASSET, dropna=False)
TSMAX = series_groupby_apply(TSMAX, by=BY_ASSET, dropna=False)
TSMIN = series_groupby_apply(TSMIN, by=BY_ASSET, dropna=False)
SUM = series_groupby_apply(SUM, by=BY_ASSET, dropna=False)
DECAYLINEAR = series_groupby_apply(DECAYLINEAR, by=BY_ASSET, dropna=False)
PROD = series_groupby_apply(PROD, by=BY_ASSET, dropna=False)
MEAN = series_groupby_apply(MEAN, by=BY_ASSET, dropna=False)
SMA = series_groupby_apply(SMA, by=BY_ASSET, dropna=False)
REGBETA = series_groupby_apply(REGBETA, by=BY_ASSET, dropna=False)
COUNT = series_groupby_apply(COUNT, by=BY_ASSET, dropna=False)
MA = series_groupby_apply(MA, by=BY_ASSET, dropna=False)

# 时序，双输入
CORR = dataframe_groupby_apply(CORR, by=BY_ASSET, dropna=True)
COVIANCE = dataframe_groupby_apply(COVIANCE, by=BY_ASSET, dropna=True)

# 截面
RANK = series_groupby_apply(RANK, by=BY_DATE, dropna=False)

LessThan = LessThan
