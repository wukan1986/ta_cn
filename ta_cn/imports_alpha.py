from .alpha import RANK as rank
from .alpha import TS_RANK as ts_rank
from .alpha import signedpower
from .logical import IF
from .maths import LOG as log
from .maths import SGN as sign
from .reference import DIFF as delta
from .reference import HHV as ts_max
from .reference import HHVBARS as ts_argmax
from .reference import LLV as ts_min
from .reference import LLVBARS as ts_argmin
from .reference import REF as delay
from .statistics import CORREL as correlation
from .statistics import COVAR as covariance
from .statistics import STDP as stddev
from .reference import SUM as sum
from .utils import to_pd, series_groupby_apply, dataframe_groupby_apply

"""
rank是横截面操作
scale呢？
"""
# 逐元素, 只需要输出由numpy转pandas即可
signedpower = to_pd(signedpower)
IF = to_pd(IF)
log = to_pd(log)
sign = to_pd(sign)

# 按股票分组，计算时序指标。注意，组内时序需要已经排序
BY_ASSET = 'asset'
# 按时间分组。计算横截面
BY_DATE = 'date'

# 时序
stddev = series_groupby_apply(stddev, by=BY_ASSET)
ts_argmax = series_groupby_apply(ts_argmax, by=BY_ASSET)
ts_argmin = series_groupby_apply(ts_argmin, by=BY_ASSET)
delta = series_groupby_apply(delta, by=BY_ASSET)
ts_rank = series_groupby_apply(ts_rank, by=BY_ASSET)
delay = series_groupby_apply(delay, by=BY_ASSET)
ts_max = series_groupby_apply(ts_max, by=BY_ASSET)
ts_min = series_groupby_apply(ts_min, by=BY_ASSET)
sum = series_groupby_apply(sum, by=BY_ASSET)

# 时序，双输入
correlation = dataframe_groupby_apply(correlation, by=BY_ASSET)
covariance = dataframe_groupby_apply(covariance, by=BY_ASSET)

# 截面
rank = series_groupby_apply(rank, by=BY_DATE)
