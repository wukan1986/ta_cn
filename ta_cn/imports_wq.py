"""
通达信公式转alpha101
"""
from functools import wraps

from .alpha import RANK as rank, demean
from .alpha import TS_RANK as ts_rank
from .alpha import scale
from .alpha import signedpower as SignedPower
from .logical import IF
from .maths import LOG as log
from .maths import MAX
from .maths import MIN
from .maths import SGN as sign
from .reference import DIFF as delta
from .reference import HHV as ts_max
from .reference import HHVBARS as ts_argmax
from .reference import LLV as ts_min
from .reference import LLVBARS as ts_argmin
from .reference import PRODUCT as product
from .reference import REF as delay
from .reference import SUM as sum
from .reference import WMA as decay_linear
from .statistics import CORREL as correlation
from .statistics import COVAR as covariance
from .statistics import STDP as stddev
from .utils import to_pd, series_groupby_apply, dataframe_groupby_apply

"""
1. 将通达信公式改名成World Quant中对应公式
2. index用于groupby，将用于实现按股票分组计算滚动指标，按时间分组计算横截面
3. 逐元素指标用装饰器返回pandas
4. 按行和按列分组，都使用装饰器
"""


def round_a_i(func):
    """将参数 向量浮点 调整成 向量整数"""

    @wraps(func)
    def decorated(a, i):
        return func(a, round(i))

    return decorated


def round_a_a_i(func):
    """将参数 向量向量浮点 调整成 向量向量整数"""

    @wraps(func)
    def decorated(a, b, i):
        return func(a, b, round(i))

    return decorated


def LessThan(x, y):
    # ValueError: Can only compare identically-labeled Series objects
    return x - y < 0


# 逐元素, 输出由numpy转pandas
SignedPower = to_pd(SignedPower)
IF = to_pd(IF)
log = to_pd(log)
sign = to_pd(sign)
MAX = to_pd(MAX)
MIN = to_pd(MIN)

# 按股票分组，计算时序指标。注意，组内时序需要已经排序
BY_ASSET = 'asset'
# 按时间分组。计算横截面
BY_DATE = 'date'
# 横截面上进行行业中性化
BY_GROUP = ['date', 'group']

# 时序
stddev = round_a_i(series_groupby_apply(stddev, by=BY_ASSET, dropna=False))
ts_argmax = round_a_i(series_groupby_apply(ts_argmax, by=BY_ASSET, dropna=False))
ts_argmin = round_a_i(series_groupby_apply(ts_argmin, by=BY_ASSET, dropna=False))
delta = round_a_i(series_groupby_apply(delta, by=BY_ASSET, dropna=False))
ts_rank = round_a_i(series_groupby_apply(ts_rank, by=BY_ASSET, dropna=False))
delay = round_a_i(series_groupby_apply(delay, by=BY_ASSET, dropna=False))
ts_max = round_a_i(series_groupby_apply(ts_max, by=BY_ASSET, dropna=False))
ts_min = round_a_i(series_groupby_apply(ts_min, by=BY_ASSET, dropna=False))
sum = round_a_i(series_groupby_apply(sum, by=BY_ASSET, dropna=False))
decay_linear = round_a_i(series_groupby_apply(decay_linear, by=BY_ASSET, dropna=False))
product = round_a_i(series_groupby_apply(product, by=BY_ASSET, dropna=False))

# 时序，双输入
correlation = round_a_a_i(dataframe_groupby_apply(correlation, by=BY_ASSET, dropna=True))
covariance = round_a_a_i(dataframe_groupby_apply(covariance, by=BY_ASSET, dropna=True))

# 截面
rank = series_groupby_apply(rank, by=BY_DATE, dropna=False)
scale = series_groupby_apply(scale, by=BY_DATE, dropna=False)

# 行业中性。demean法
indneutralize = dataframe_groupby_apply(demean, by=BY_GROUP, dropna=False)

## 部分别名，这样官方公式可以减少改动
Ts_Rank = ts_rank
IndNeutralize = indneutralize
Ts_ArgMax = ts_argmax
Ts_ArgMin = ts_argmin
