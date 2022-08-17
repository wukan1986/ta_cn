"""
通达信公式转alpha101

101 Formulaic Alphas
文档质量一般
1. 部分函数即有全小写，又有大小写混合
2. 很多参数应当是整数，但输入是小数，不得不做修正
"""
from functools import wraps

import ta_cn.talib as ta

_ta1d = ta.init(mode=1, skipna=False)

correlation = _ta1d.CORREL
decay_linear = _ta1d.WMA

from ta_cn.alpha import LessThan
from ta_cn.alpha import RANK as rank
from ta_cn.alpha import TS_RANK as ts_rank
from ta_cn.alpha import scale
from ta_cn.alpha import signedpower as SignedPower
from ta_cn.logical import IF
from ta_cn.maths import LN as log  # 引入的是自然对数
from ta_cn.maths import MAX
from ta_cn.maths import MIN
from ta_cn.maths import SGN as sign
from ta_cn.preprocess import demean
from ta_cn.reference import DIFF as delta
from ta_cn.reference import HHV as ts_max
from ta_cn.reference import HHVBARS as ts_argmax
from ta_cn.reference import LLV as ts_min
from ta_cn.reference import LLVBARS as ts_argmin
from ta_cn.reference import PRODUCT as product
from ta_cn.reference import REF as delay
from ta_cn.reference import SUM as sum
from ta_cn.statistics import COVAR as covariance
from ta_cn.statistics import STDP as stddev  # 引入的是全体标准差
from ta_cn.utils import to_pd
from ta_cn.utils_long import series_groupby_apply, dataframe_groupby_apply

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

dropna = False

# 时序
stddev = round_a_i(series_groupby_apply(stddev, by=BY_ASSET))
ts_argmax = round_a_i(series_groupby_apply(ts_argmax, by=BY_ASSET))
ts_argmin = round_a_i(series_groupby_apply(ts_argmin, by=BY_ASSET))
delta = round_a_i(series_groupby_apply(delta, by=BY_ASSET))
ts_rank = round_a_i(series_groupby_apply(ts_rank, by=BY_ASSET))
delay = round_a_i(series_groupby_apply(delay, by=BY_ASSET))
ts_max = round_a_i(series_groupby_apply(ts_max, by=BY_ASSET))
ts_min = round_a_i(series_groupby_apply(ts_min, by=BY_ASSET))
sum = round_a_i(series_groupby_apply(sum, by=BY_ASSET))
decay_linear = round_a_i(series_groupby_apply(decay_linear, by=BY_ASSET))
product = round_a_i(series_groupby_apply(product, by=BY_ASSET))

# 时序，双输入
correlation = round_a_a_i(dataframe_groupby_apply(correlation, by=BY_ASSET, to_df=[0, 1], to_kwargs={2: 'timeperiod'}))
covariance = round_a_a_i(dataframe_groupby_apply(covariance, by=BY_ASSET, to_df=[0, 1], to_kwargs={2: 'timeperiod'}))

# 截面
rank = series_groupby_apply(rank, by=BY_DATE, to_kwargs={})
scale = series_groupby_apply(scale, by=BY_DATE, to_kwargs={1: 'a'})

# 行业中性。demean法
indneutralize = dataframe_groupby_apply(demean, by=BY_GROUP, to_df=[0, 'group'], to_kwargs={})

# 部分别名，这样官方公式可以减少改动
Ts_Rank = ts_rank
IndNeutralize = indneutralize
Ts_ArgMax = ts_argmax
Ts_ArgMin = ts_argmin
LessThan = LessThan
min = MIN
max = MAX
Sign = sign
Log = log
