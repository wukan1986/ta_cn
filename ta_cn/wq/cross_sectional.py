"""
Cross Sectional Operators
"""
import numpy as np

from .arithmetic import add, abs_
from .. import bn_wraps as bn
from ..utils import pd_to_np


def normalize(x, useStd=False, limit=0.0):
    """Calculates the mean value of all valid alpha values for a certain date, then subtracts that mean from each element."""
    axis = x.ndim - 1
    t1 = np.nanmean(x, axis=axis, keepdims=True)
    if useStd:
        # 这里用ddof=1才能与文档示例的数值对应上
        t2 = np.nanstd(x, axis=axis, keepdims=True, ddof=1)
        r = (x - t1) / t2
    else:
        r = (x - t1)

    return r if limit == 0 else np.clip(r, -limit, limit)


def one_side(x, side='long'):
    """Shifts all instruments up or down so that the Alpha becomes long-only or short-only
(if side = short), respectively."""
    # TODO: 这里不确定，需再研究
    # [-1, 0, 1]+1=[0, 1, 2]
    # max([-1, 0, 1], 0)=[0,0,1]
    if side == 'long':
        return np.maximum(x, 0)
    else:
        return np.minimum(x, 0)


def quantile(x, driver='gaussian', sigma=1.0):
    """Rank the raw vector, shift the ranked Alpha vector, apply distribution ( gaussian, cauchy, uniform ). If driver is uniform, it simply subtract each Alpha value with the mean of all Alpha values in the Alpha vector."""
    pass


def rank(x, rate=2, pct=True):
    """Ranks the input among all the instruments and returns an equally distributed number between 0.0 and 1.0. For precise sort, use the rate as 0."""
    axis = x.ndim - 1
    t1 = bn.nanrankdata(x, axis=axis)

    if pct:
        t2 = np.nansum(~np.isnan(x), axis=axis, keepdims=True)

        return t1 / t2
    else:
        return t1


def rank_by_side(x, rate=2, scale=1):
    """Ranks positive and negative input separately and scale to book. For precise sorting use rate=0."""
    pass


def generalized_rank(open, m=1):
    """The idea is that difference between instrument values raised to the power of m is added to the rank of instrument with bigger value and subtracted from the rank of instrument with lesser value. More details in the notes at the end of page."""
    pass


def regression_neut(y, x):
    """Conducts the cross-sectional regression on the stocks with Y as target and X as the independent variable."""
    pass


def regression_proj(y, x):
    """Conducts the cross-sectional regression on the stocks with Y as target and X as the independent variable."""
    pass


def scale(x, scale=1, longscale=1, shortscale=1):
    """Scales input to booksize. We can also scale the long positions and short positions to separate scales by mentioning additional parameters to the operator."""
    if longscale != 1 or shortscale != 1:
        L = np.where(x > 0, x, np.nan)
        S = np.where(x < 0, x, np.nan)

        sum_l = np.nansum(abs_(L), axis=x.ndim - 1, keepdims=True)
        sum_s = np.nansum(abs_(S), axis=x.ndim - 1, keepdims=True)

        with np.errstate(divide='ignore', invalid='ignore'):
            return add(L / sum_l * longscale, S / sum_s * shortscale, filter=True)
    else:
        sum_x = np.nansum(abs_(x), axis=x.ndim - 1, keepdims=True)
        with np.errstate(divide='ignore', invalid='ignore'):
            return x / sum_x * scale


def scale_down(x, constant=0):
    """Scales all values in each day proportionately between 0 and 1 such that minimum value maps to 0 and maximum value maps to 1. Constant is the offset by which final result is subtracted."""
    axis = x.ndim - 1
    m1 = np.nanmin(x, axis=axis, keepdims=True)
    m2 = np.nanmax(x, axis=axis, keepdims=True)

    return (x - m1) / (m2 - m1) - constant


def truncate(x, maxPercent=0.01):
    """Operator truncates all values of x to maxPercent. Here, maxPercent is in decimal notation."""
    axis = x.ndim - 1
    t1 = np.nansum(x, axis=axis, keepdims=True) * maxPercent

    return np.minimum(x, t1)


def vector_neut(x, y):
    """For given vectors x and y, it finds a new vector x* (output) such that x* is orthogonal to y."""
    pass


def vector_proj(x, y):
    """Returns vector projection of x onto y. Algebraic and geometric details can be found on wiki"""
    pass


def winsorize(x, std=4):
    """Winsorizes x to make sure that all values in x are between the lower and upper limits, which are specified as multiple of std. Details can be found on wiki"""
    x = pd_to_np(x, copy=False)
    axis = x.ndim - 1
    _mean = np.nanmean(x, axis=axis, keepdims=True)
    _std = np.nanstd(x, axis=axis, keepdims=True, ddof=0) * std

    return np.clip(x, _mean - _std, _mean + _std)


def zscore(x):
    """Z-score is a numerical measurement that describes a value's relationship to the mean of a group of values. Z-score is measured in terms of standard deviations from the mean"""
    x = pd_to_np(x, copy=False)
    axis = x.ndim - 1
    _mean = np.nanmean(x, axis=axis, keepdims=True)
    _std = np.nanstd(x, axis=axis, keepdims=True, ddof=0)

    return (x - _mean) / _std


def rank_gmean_amean_diff(*args):
    """Operator returns difference of geometric mean and arithmetic mean of cross sectional rank of inputs."""

    # TODO: 输入输出的形式还没搞清，核心功能已经实现先放这
    def _gmean(x):
        return np.exp(np.nanmean(np.log(x)))

    inputs = rank(np.array(args))
    inputs = np.array(args)
    return _gmean(inputs) - np.nanmean(inputs)
