import numba
import numpy as _np

from .utils import pd_to_np


@numba.jit(nopython=True, cache=True, nogil=True)
def _filter_nb(arr, n):
    """内部函数，请勿直接调用，请参考"""
    is_1d = arr.ndim == 1
    x = arr.shape[0]
    y = 1 if is_1d else arr.shape[1]

    for j in range(y):
        a = arr if is_1d else arr[:, j]

        # 为了跳过不必要部分，由for改while
        i = 0
        while i < x:
            if a[i]:
                a[i + 1:i + 1 + n] = 0
                i += n + 1
            else:
                i += 1
    return arr


@numba.jit(nopython=True, cache=True, nogil=True)
def _bars_last_nb(arr, out):
    """上一次条件成立到当前的周期数"""
    is_1d = arr.ndim == 1
    x = arr.shape[0]
    y = 1 if is_1d else arr.shape[1]

    for j in range(y):
        a = arr if is_1d else arr[:, j]
        b = out if is_1d else out[:, j]
        s = 0
        for i in range(x):
            if a[i]:
                s = 0
            b[i] = s
            s += 1

    return out


@numba.jit(nopython=True, cache=True, nogil=True)
def _bars_last_count_nb(arr, out):
    """

    Parameters
    ----------
    arr
    out

    References
    ----------
    https://stackoverflow.com/questions/18196811/cumsum-reset-at-nan

    """
    is_1d = arr.ndim == 1
    x = arr.shape[0]
    y = 1 if is_1d else arr.shape[1]

    for j in range(y):
        a = arr if is_1d else arr[:, j]
        b = out if is_1d else out[:, j]
        s = 0
        for i in range(x):
            if a[i]:
                s += 1
                b[i] = s
            else:
                s = 0

    return out


@numba.jit(nopython=True, cache=True, nogil=True)
def _fill_notna_nb(arr, fill_value, n: int):
    is_1d = arr.ndim == 1
    x = arr.shape[0]
    y = 1 if is_1d else arr.shape[1]

    for j in range(y):
        a = arr if is_1d else arr[:, j]
        k = n
        for i in range(x):
            if _np.isnan(a[i]):
                continue
            a[i] = fill_value
            k -= 1
            if k <= 0:
                break

    return arr


@numba.jit(nopython=True, cache=True, nogil=True)
def _sum_1st_nb(arr, n):
    """前部分数据求和，之前的设置成0"""
    is_1d = arr.ndim == 1
    x = arr.shape[0]
    y = 1 if is_1d else arr.shape[1]

    for j in range(y):
        a = arr if is_1d else arr[:, j]
        k = n
        s = 0.0
        skip_nan = True
        for i in range(x):
            if _np.isnan(a[i]):
                if skip_nan:
                    continue
                else:
                    a[i] = 0
            skip_nan = False
            s += a[i]
            a[i] = 0
            k -= 1
            if k <= 0:
                a[i] = s
                break
    return arr


@numba.jit(nopython=True, cache=True, nogil=True)
def _ma_1st_nb(arr, n):
    """前部分数据求和，之前的设置成0"""
    is_1d = arr.ndim == 1
    x = arr.shape[0]
    y = 1 if is_1d else arr.shape[1]

    for j in range(y):
        a = arr if is_1d else arr[:, j]
        k = n
        s = 0.0
        for i in range(x):
            if _np.isnan(a[i]):
                continue
            s += a[i]
            a[i] = _np.nan
            k -= 1
            if k <= 0:
                a[i] = s / n
                break
    return arr


def fill_notna(arr, fill_value, n=1):
    """查找第一个非nan,将其改成fill_value"""
    if n < 1:
        return arr
    arr = pd_to_np(arr, copy=True)
    return _fill_notna_nb(arr, fill_value, n)


def ma_1st(arr, n=1):
    """前部分数据求平均，之前的设置成np.nan"""
    if n < 1:
        return arr
    arr = pd_to_np(arr, copy=True)
    return _ma_1st_nb(arr, n)


def sum_1st(arr, n=1):
    """前部分数据求平均，之前的设置成np.nan"""
    if n < 1:
        return arr
    arr = pd_to_np(arr, copy=True)
    return _sum_1st_nb(arr, n)


@numba.jit(nopython=True, cache=True, nogil=True)
def _avedev_nb(a):
    """avedev平均绝对偏差"""
    return _np.mean(_np.abs(a - _np.mean(a)))


@numba.jit(nopython=True, cache=True, nogil=True)
def _bars_since_n_nb(a, n):
    """BARSSINCEN(X,N):N周期内第一次X不为0到现在的天数"""
    for i, x in enumerate(a):
        if x:
            return n - i - 1
    return 0


@numba.jit(nopython=True, cache=True, nogil=True)
def _slope_nb(y, x, m_x):
    """slope线性回归斜率"""
    m_y = _np.mean(y)
    return _np.sum((x - m_x) * (y - m_y)) / _np.sum((x - m_x) ** 2)


@numba.jit(nopython=True, cache=True, nogil=True)
def _rolling_func_nb(arr, out, timeperiod, func, *args):
    """滚动函数"""
    if arr.ndim == 3:
        for i, aa in enumerate(arr):
            for j, a in enumerate(aa):
                out[i + timeperiod - 1, j] = func(a, *args)
    elif arr.ndim == 2:
        for i, a in enumerate(arr):
            out[i + timeperiod - 1] = func(a, *args)

    return out


def numpy_rolling_apply(data, window, func1, func2, *args):
    """滚动应用方法"""
    arr = _np.lib.stride_tricks.sliding_window_view(data, window, axis=0)
    out = _np.empty_like(data)

    try:
        out[:window] = _np.nan
    except:
        out[:window] = 0

    return func1(arr, out, window, func2, *args)
