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
    return arr


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


def _filter(S, N):
    """FILTER函数，S满足条件后，将其后N周期内的数据置为0"""
    S = pd_to_np(S, copy=True)
    return _filter_nb(S, N)


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
