import numba
import numpy as np

from ta_cn.utils import pd_to_np


@numba.jit(nopython=True, cache=True, nogil=True)
def ewm_mean_1d_nb(a, out, alpha, minp: int = 0, adjust: bool = False):
    """Return exponential weighted average.
    Numba equivalent to `pd.Series(a).ewm(span=span, min_periods=minp, adjust=adjust).mean()`.
    Adaptation of `pd._libs.window.aggregations.window_aggregations.ewma` with default arguments."""
    N = len(a)
    old_wt_factor = 1. - alpha
    new_wt_factor = alpha
    weighted_avg = a[0]
    is_observation = (weighted_avg == weighted_avg)
    nobs = int(is_observation)
    out[0] = weighted_avg if (nobs >= minp) else np.nan
    old_wt = 1.

    for i in range(1, N):
        cur = a[i]
        is_observation = (cur == cur)  # 非NaN
        nobs += is_observation

        if weighted_avg == weighted_avg:
            old_wt *= old_wt_factor[i]
            new_wt = new_wt_factor[i]
            if is_observation:
                # avoid numerical errors on constant series
                if weighted_avg != cur:
                    weighted_avg = ((old_wt * weighted_avg) + (new_wt * cur)) / (old_wt + new_wt)
                if adjust:
                    old_wt += new_wt
                else:
                    old_wt = 1.
        elif is_observation:
            weighted_avg = cur
        out[i] = weighted_avg if (nobs >= minp) else np.nan
    return out


@numba.jit(nopython=True, cache=True, nogil=True)
def ewm_mean_nb(a, out, alpha, minp: int = 0, adjust: bool = False):
    """2-dim version of `ewm_mean_1d_nb`."""
    for col in range(a.shape[1]):
        out[:, col] = ewm_mean_1d_nb(a[:, col], out[:, col], alpha[:, col], minp=minp, adjust=adjust)
    return out


def ewm_mean(a, alpha=None, span=None, com=None, min_periods: int = 0, adjust: bool = False):
    """指数移动平均

    pandas使用cython技术，本处使用numba。实测发现numba版更快

    Parameters
    ----------
    a
    alpha
    span
    com
    min_periods
    adjust:
        是否使用调整算法。一般使用False

    References
    ----------
    https://github.com/pandas-dev/pandas/blob/main/pandas/_libs/window/aggregations.pyx
    https://github.com/polakowo/vectorbt/blob/master/vectorbt/generic/nb.py

    """
    # 三个参数只使用其中一个即可
    if span is not None:
        com = (span - 1) / 2.0
    if com is not None:
        alpha = 1. / (1. + com)

    a = pd_to_np(a)
    out = np.empty_like(a)

    if isinstance(alpha, (int, float)):
        # 单数字就扩展
        alpha = np.full_like(a, fill_value=alpha)

    if a.ndim == 2:
        return ewm_mean_nb(a, out, alpha, minp=min_periods, adjust=adjust)
    else:
        return ewm_mean_1d_nb(a, out, alpha, minp=min_periods, adjust=adjust)
