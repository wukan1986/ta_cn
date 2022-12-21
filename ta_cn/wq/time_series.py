"""
Time Series Operators
"""
import numba
import numpy as np
from numba.typed import List

from .. import bn_wraps as bn
from .. import talib as ta
from ..nb import numpy_rolling_apply, _rolling_func_1_nb, _rolling_func_2_nb, _rolling_func_3_nb
from ..regress import ts_simple_regress
from ..utils import pd_to_np

_ta1d = ta.init(mode=1, skipna=False, to_globals=False)
_ta2d = ta.init(mode=2, skipna=False, to_globals=False)


@numba.jit(nopython=True, cache=True, nogil=True)
def _days_from_last_change_nb(arr, out):
    is_1d = arr.ndim == 1
    x = arr.shape[0]
    y = 1 if is_1d else arr.shape[1]

    for j in range(y):
        a = arr if is_1d else arr[:, j]
        b = out if is_1d else out[:, j]
        last = a[0]
        k = 0
        for i in range(1, x):
            cur = a[i]
            if cur == last:
                k += 1
            else:
                last = cur
                k = 0
            b[i] = k

    return out


def days_from_last_change(x):
    """Amount of days since last change of x"""

    x = pd_to_np(x, copy=False)
    out = np.zeros_like(x, dtype=int)
    return _days_from_last_change_nb(x, out)


def ts_weighted_delay(x, k=0.5):
    """Instead of replacing today’s value with yesterday’s as in ts_delay(x, 1), it assigns weighted average of today’s and yesterday’s values with weight on today’s value being k and yesterday’s being (1-k)."""
    pass


def hump(x, hump=0.01):
    """Limits amount and magnitude of changes in input (thus reducing turnover)."""
    pass


def hump_decay(x, p=0, relative=False):
    """This operator helps to ignore the values that changed too little corresponding to previous ones."""
    t1 = ts_delay(x, 1)
    t2 = abs(x - t1)
    if relative:
        t3 = abs(x + t1)
        return np.where(t2 > (p * t3), x, t1)
    else:
        return np.where(t2 > p, x, t1)


def inst_tvr(x, d):
    """Total trading value / Total holding value in the past d days"""
    pass


def jump_decay(x, d, stddev=False, sensitivity=0.5, force=0.1):
    """If there is a huge jump in current data compare to previous one"""
    std = 1 if not stddev else ts_std_dev(x, d)
    t0 = ts_delay(x, 1)
    t1 = abs(x - t0) > sensitivity * std
    t2 = t0 + (x - t0) * force

    return np.where(t1, t2, x)


# TODO: 需要再验证
@numba.jit(nopython=True, cache=True, nogil=True)
def _kth_element_nb(arr, k, ignore):
    for a in arr[-1 - k::-1]:
        if a == a:
            for i in ignore:
                if a == i:
                    continue
                else:
                    return a
        else:
            for i in ignore:
                if i != i:
                    continue


def kth_element(x, d, k=1, ignore=[]):
    """Returns K-th value of input by looking through lookback days. This operator can be used to backfill missing data if k=1"""

    # 由于原文档中数据需要[::-1]，所以backfill其实是ffill
    # ignore参数用来计数时跳过，文档不对应
    return numpy_rolling_apply([pd_to_np(x)],
                               d, _rolling_func_1_nb, _kth_element_nb,
                               k, List(ignore))


@numba.jit(nopython=True, cache=True, nogil=True)
def _last_diff_value_nb(arr):
    l = arr[-1]
    for a in arr[::-1]:
        if a != l:
            return a
    return l


def last_diff_value(x, d):
    """Returns last x value not equal to current x value from last d days"""
    return numpy_rolling_apply([pd_to_np(x)],
                               d, _rolling_func_1_nb, _last_diff_value_nb)


def ts_arg_max(x, d):
    """Returns the relative index of the min value in the time series for the past d days. If the current day has the min value for the past d days, it returns 0. If previous day has the min value for the past d days, it returns 1."""
    # 文档中的数据其实要[::-1]
    return bn.move_argmax(x, window=d, axis=0)


def ts_arg_min(x, d):
    """Returns the relative index of the min value in the time series for the past d days; If the current day has the min value for the past d days, it returns 0; If previous day has the min value for the past d days, it returns 1"""
    return bn.move_argmin(x, window=d, axis=0)


def ts_av_diff(x, d):
    """Returns x - tsmean(x, d), but deals with NaNs carefully. That is NaNs are ignored during mean computation."""

    def _ts_mean(x, d):
        """Returns average value of x for the past d days."""
        # 这里为了跳过空值
        t1 = bn.move_sum(np.nan_to_num(x), window=d, axis=0)
        t2 = bn.move_sum(~np.isnan(x), window=d, axis=0)
        return t1 / t2

    # 平均数的计算要跳过NaN
    return x - _ts_mean(x, d)


def ts_backfill(x, lookback=10, k=1, ignore="NAN"):
    """Backfill is the process of replacing the NAN or 0 values by a meaningful value (i.e., a first non-NaN value)"""
    pass


@numba.jit(nopython=True, cache=True, nogil=True)
def _co_kurtosis_nb(arr0, arr1):
    t1 = arr0 - np.nanmean(arr0)
    t2 = arr1 - np.nanmean(arr1)
    t3 = np.nanstd(arr0)
    t4 = np.nanstd(arr1)
    return np.nanmean(t1 * (t2 ** 3)) / (t3 * (t4 ** 3))


def ts_co_kurtosis(y, x, d):
    """Returns cokurtosis of y and x for the past d days."""
    return numpy_rolling_apply([pd_to_np(y), pd_to_np(x)],
                               d, _rolling_func_2_nb, _co_kurtosis_nb)


@numba.jit(nopython=True, cache=True, nogil=True)
def _corr_nb(arr0, arr1):
    return np.corrcoef(arr0, arr1)[0, 1]


def ts_corr(x, y, d):
    """Returns correlation of x and y for the past d days"""
    if True:
        return _ta2d.CORREL(x, y, timeperiod=d)
    else:
        return numpy_rolling_apply([pd_to_np(x), pd_to_np(y)],
                                   d, _rolling_func_2_nb, _corr_nb)


@numba.jit(nopython=True, cache=True, nogil=True)
def _co_skewness_nb(arr0, arr1):
    t1 = arr0 - np.nanmean(arr0)
    t2 = arr1 - np.nanmean(arr1)
    t3 = np.nanstd(arr0)
    t4 = np.nanstd(arr1)
    return np.nanmean(t1 * (t2 ** 2)) / (t3 * (t4 ** 2))


def ts_co_skewness(y, x, d):
    """Returns coskewness of y and x for the past d days."""
    return numpy_rolling_apply([pd_to_np(y), pd_to_np(x)],
                               d, _rolling_func_2_nb, _co_skewness_nb)


def ts_count_nans(x, d):
    """Returns the number of NaN values in x for the past d days"""
    return ts_sum(np.isnan(x), d)


@numba.jit(nopython=True, cache=True, nogil=True)
def _covariance_nb(arr0, arr1):
    """协方差矩阵"""
    return np.cov(arr0, arr1)[0, 1]


def ts_covariance(y, x, d):
    """Returns covariance of y and x for the past d days"""
    return numpy_rolling_apply([pd_to_np(y), pd_to_np(x)],
                               d, _rolling_func_2_nb, _covariance_nb)


def ts_decay_exp_window(x, d, factor=0.5):
    """Returns exponential decay of x with smoothing factor for the past d days."""
    pass


def ts_decay_linear(x, d, dense=True):
    """Returns the linear decay on x for the past d days. Dense parameter=false means operator works in sparse mode and we treat NaN as 0. In dense mode we do not."""
    # TODO: 这样写是否合适？
    if dense:
        return _ta2d.WMA(x, timeperiod=d)
    else:
        return _ta2d.WMA(np.nan_to_num(x), timeperiod=d)


def ts_delay(x, d):
    """Returns x value d days ago"""
    if d == 0 or np.isnan(d):
        # 该不该复制呢？
        return x
    arr = np.empty_like(x)
    fill_value = 0 if np.issubdtype(arr.dtype, np.integer) else np.nan
    if d > 0:
        arr[:d] = fill_value
        arr[d:] = x[:-d]
    if d < 0:
        # 为了复刻shift(-n)
        arr[d:] = fill_value
        arr[:d] = x[-d:]
    return arr


def ts_delta(x, d):
    """Returns x - ts_delay(x, d)"""
    return x - ts_delay(x, d)


def ts_ir(x, d):
    """Return information ratio ts_mean(x, d) / ts_std_dev(x, d)"""
    return ts_mean(x, d) / ts_std_dev(x, d)


# # 与scipy.stats.kurtosis结果相同，与pd.rolling.kurt结果不同, bias的问题
@numba.jit(nopython=True, cache=True, nogil=True)
def _kurtosis_nb(arr):
    t1 = arr - np.nanmean(arr)
    return np.nanmean(t1 ** 4) / (np.nanmean(t1 ** 2) ** 2)


def ts_kurtosis(x, d):
    """Returns kurtosis of x for the last d days."""
    return numpy_rolling_apply([pd_to_np(x)], d, _rolling_func_1_nb, _kurtosis_nb) - 3


def ts_max(x, d):
    """Returns max value of x for the past d days"""
    return bn.move_max(x, window=d, axis=0)


def ts_max_diff(x, d):
    """Returns x - ts_max(x, d)"""
    return x - ts_max(x, d)


def ts_mean(x, d):
    """Returns average value of x for the past d days."""
    return bn.move_mean(x, window=d, axis=0)


def ts_median(x, d):
    """Returns median value of x for the past d days"""
    return bn.move_median(x, window=d, axis=0)


def ts_min(x, d):
    """Returns min value of x for the past d days"""
    return bn.move_min(x, window=d, axis=0)


def ts_min_diff(x, d):
    """Returns x - ts_min(x, d)"""
    return x - ts_min(x, d)


def ts_min_max_cps(x, d, f=2):
    """Returns (ts_min(x, d) + ts_max(x, d)) - f * x. If not specified, by default f = 2"""
    return (ts_min(x, d) + ts_max(x, d)) - f * x


def ts_min_max_diff(x, d, f=0.5):
    """Returns x - f * (ts_min(x, d) + ts_max(x, d)). If not specified, by default f = 0.5"""
    return x - f * (ts_min(x, d) + ts_max(x, d))


@numba.jit(nopython=True, cache=True, nogil=True)
def _moment_nb(arr, k):
    """中心矩阵"""
    return np.nanmean((arr - np.nanmean(arr)) ** k)


def ts_moment(x, d, k=0):
    """Returns K-th central moment of x for the past d days."""

    if k == 2:
        # 结果是一样的，使用计算更快的版本
        return bn.move_var(x, window=d, axis=0)
    # 计算K阶中心矩
    return numpy_rolling_apply([pd_to_np(x)], d, _rolling_func_1_nb, _moment_nb, k)


# TODO: 不知道是否写正确，需要check
@numba.jit(nopython=True, cache=True, nogil=True)
def _partial_corr_nb(arr0, arr1, arr2):
    c = np.corrcoef(np.vstack((arr0, arr1, arr2)))
    rxy = c[0, 1]
    rxz = c[0, 2]
    ryz = c[1, 2]
    t1 = rxy - rxz * ryz
    t2 = (1 - rxz ** 2) ** 0.5
    t3 = (1 - ryz ** 2) ** 0.5
    return t1 / (t2 * t3)


def ts_partial_corr(x, y, z, d):
    """Returns partial correlation of x, y, z for the past d days."""

    return numpy_rolling_apply([pd_to_np(x), pd_to_np(y), pd_to_np(z)],
                               d, _rolling_func_3_nb, _partial_corr_nb)


@numba.jit(nopython=True, cache=True, nogil=True)
def _percentage_nb(a, percentage):
    return np.quantile(a, percentage)


def ts_percentage(x, d, percentage=0.5):
    """Returns percentile value of x for the past d days."""
    return numpy_rolling_apply([pd_to_np(x)], d, _rolling_func_1_nb, _percentage_nb, percentage)


def ts_poly_regression(y, x, d, k=1):
    """Returns y - Ey, where Ey = x + x^2 + … + x^k over d days; k must be specified as a keyword argument"""
    pass


@numba.jit(nopython=True, cache=True, nogil=True)
def _product_nb(a):
    return np.nanprod(a)


def ts_product(x, d):
    """Returns product of x for the past d days"""
    return numpy_rolling_apply([pd_to_np(x)], d, _rolling_func_1_nb, _product_nb)


def ts_rank(x, d, constant=0):
    """Rank the values of x for each instrument over the past d days, then return the rank of the current value + constant. If not specified, by default, constant = 0."""
    # 取值范围是闭区间[0,1]
    t1 = bn.move_rank(x, window=d, axis=0)
    return (t1 + 1) / 2 + constant


def ts_regression(y, x, d, lag=0, rettype=0):
    """Returns various parameters related to regression function."""
    return ts_simple_regress(y, x, d, lag=lag, rettype=rettype)


def ts_returns(x, d, mode=1):
    """Returns the relative change in the x value ."""
    if d >= 0:
        t1 = ts_delay(x, d)
        if mode == 1:
            return x / t1 - 1.
        if mode == 2:
            return (x - t1) / ((x + t1) / 2)
    else:
        # 负数相当于pct_change(d).shift(-d),用于机器学习打标签
        t1 = ts_delay(x, d)
        if mode == 1:
            return t1 / x - 1


def ts_scale(x, d, constant=0):
    """Returns (x – ts_min(x, d)) / (ts_max(x, d) – ts_min(x, d)) + constant
This operator is similar to scale down operator but acts in time series space."""
    t1 = ts_min(x, d)
    t2 = ts_max(x, d)
    return (x - t1) / (t2 - t1) + constant


# 与scipy.stats.skew结果相同，与pd.rolling.skew结果不同, bias的问题
@numba.jit(nopython=True, cache=True, nogil=True)
def _skewness_nb(arr):
    t1 = arr - np.nanmean(arr)
    return np.nanmean(t1 ** 3) / (np.nanmean(t1 ** 2) ** 1.5)


def ts_skewness(x, d):
    """Return skewness of x for the past d days."""
    return numpy_rolling_apply([pd_to_np(x)], d, _rolling_func_1_nb, _skewness_nb)


def ts_std_dev(x, d):
    """Returns standard deviation of x for the past d days"""
    # 长表与宽表计算居然结果有微小差异
    # return bn.move_std(x, window=d, axis=0, ddof=0)
    if x.ndim == 2:
        return _ta2d.STDDEV(x, timeperiod=d)
    else:
        return _ta1d.STDDEV(x, timeperiod=d)


def ts_step(d):
    """Returns days' counter"""
    # TODO: 这种如何应用是个问题
    return np.arange(d)


def ts_sum(x, d):
    """Sum values of x for the past d days."""
    if d > 0:
        return bn.move_sum(x, window=d, axis=0)
    else:
        # 0表示全量累计求和，这是为通达信公式服务
        return np.cumsum(x, axis=0)


def ts_theilsen(x, y, d):
    """Theil Sen slope estimator of inputs for the past n days."""
    pass


@numba.jit(nopython=True, cache=True, nogil=True)
def _triple_corr_nb(arr0, arr1, arr2):
    t1 = arr0 - np.nanmean(arr0)
    t2 = arr1 - np.nanmean(arr1)
    t3 = arr2 - np.nanmean(arr2)
    t4 = np.nanstd(arr0)
    t5 = np.nanstd(arr1)
    t6 = np.nanstd(arr2)
    return np.nanmean(t1 * t2 * t3) / (t4 * t5 * t6)


def ts_triple_corr(x, y, z, d):
    """Returns triple correlation of x, y, z for the past d days."""
    return numpy_rolling_apply([pd_to_np(x), pd_to_np(y), pd_to_np(z)],
                               d, _rolling_func_3_nb, _triple_corr_nb)


def ts_zscore(x, d):
    """Z-score is a numerical measurement that describes a value's relationship to the mean of a group of values. Z-score is measured in terms of standard deviations from the mean: (x - tsmean(x,d)) / tsstddev(x,d)"""
    return (x - ts_mean(x, d)) / ts_std_dev(x, d)


def ts_entropy(x, d, buckets=10):
    """For each instrument, we collect values of input in the past d days and calculate the probability distribution then the information entropy via a histogram as a result."""
    pass


def ts_vector_neut(x, y, d):
    """Returns x- ts_vector_proj(x,y,d)"""
    return x - ts_vector_proj(x, y, d)


def ts_vector_proj(x, y, d):
    """Returns vector projection of x onto y in time-series space. Algebraic and geometric details can be found on wiki"""
    pass


def ts_rank_gmean_amean_diff(input1, input2, input3, d):
    """Returns Geometric Mean of ts_rank(input,d) of all input - Arithmetic Mean of ts_rank(input,d) of all input. This is similar to rank_gmean_amean_diff operator but in time-series space."""
    pass


# 与ts_percentage区别是什么，缺失一个参数是什么？
@numba.jit(nopython=True, cache=True, nogil=True)
def _quantile_nb(a, q):
    return np.quantile(a, q)


def ts_quantile(x, d, driver="gaussian"):
    """It calculates ts_rank and apply to its value an inverse cumulative density function from driver distribution. Possible values of driver (optional ) are "gaussian", "uniform", "cauchy" distribution where "gaussian" is the default."""
    return numpy_rolling_apply([pd_to_np(x)], d, _rolling_func_1_nb, _quantile_nb, 0.5)


# ------------------------


# 其它功能别名
ts_count = ts_sum


def ts_log_returns(x, d):
    """数收益率"""
    if d >= 0:
        t1 = ts_delay(x, d)
        return np.log(x / t1)
    else:
        # 负数相当于最后shift(-d)
        t1 = ts_delay(x, d)
        return np.log(t1 / x)
