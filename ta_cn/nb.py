import numba
import numpy as np

from .utils import pd_to_np


@numba.jit(nopython=True, cache=True, nogil=True)
def _fill_notna_nb(arr, fill_value, n: int):
    is_1d = arr.ndim == 1
    x = arr.shape[0]
    y = 1 if is_1d else arr.shape[1]

    for j in range(y):
        a = arr if is_1d else arr[:, j]
        k = n
        for i in range(x):
            cur = a[i]
            if cur != cur:
                continue
            a[i] = fill_value
            k -= 1
            if k <= 0:
                break

    return arr


def fill_notna(arr, fill_value, n=1):
    """查找第一个非nan,将其改成fill_value"""

    if n < 1:
        return arr
    arr = pd_to_np(arr, copy=True)
    return _fill_notna_nb(arr, fill_value, n)


@numba.jit(nopython=True, cache=True, nogil=True)
def _rolling_func_3_nb(arr0, arr1, arr2, out, timeperiod, func, *args):
    """滚动函数，在二维或三维数上遍历，三组输入

    Parameters
    ----------
    arr0:
        输入。二维或三维
    out:
        输出。一维或二维。降了一个维度
    window: int
        窗口长度
    func:
        单向量处理函数
    args:
        func的位置参数

    Returns
    -------
    np.ndarray
        一维或二维数组

    """
    if arr0.ndim == 3:
        for i, (aa, bb, cc) in enumerate(zip(arr0, arr1, arr2)):
            for j, (a, b, c) in enumerate(zip(aa, bb, cc)):
                out[i + timeperiod - 1, j] = func(a, b, c, *args)
    elif arr0.ndim == 2:
        for i, (a, b, c) in enumerate(zip(arr0, arr1, arr2)):
            out[i + timeperiod - 1] = func(a, b, c, *args)

    return out


@numba.jit(nopython=True, cache=True, nogil=True)
def _rolling_func_2_nb(arr0, arr1, out, timeperiod, func, *args):
    """滚动函数，在二维或三维数上遍历，二组输入

    Parameters
    ----------
    arr0:
        输入。二维或三维
    out:
        输出。一维或二维。降了一个维度
    window: int
        窗口长度
    func:
        单向量处理函数
    args:
        func的位置参数

    Returns
    -------
    np.ndarray
        一维或二维数组

    """
    if arr0.ndim == 3:
        for i, (aa, bb) in enumerate(zip(arr0, arr1)):
            for j, (a, b) in enumerate(zip(aa, bb)):
                out[i + timeperiod - 1, j] = func(a, b, *args)
    elif arr0.ndim == 2:
        for i, (a, b) in enumerate(zip(arr0, arr1)):
            out[i + timeperiod - 1] = func(a, b, *args)

    return out


@numba.jit(nopython=True, cache=True, nogil=True)
def _rolling_func_1_nb(arr, out, timeperiod, func, *args):
    """滚动函数，在二维或三维数上遍历，一组输入

    Parameters
    ----------
    arr:
        输入。二维或三维
    out:
        输出。一维或二维。降了一个维度
    window: int
        窗口长度
    func:
        单向量处理函数
    args:
        func的位置参数

    Returns
    -------
    np.ndarray
        一维或二维数组

    """
    if arr.ndim == 3:
        for i, aa in enumerate(arr):
            for j, a in enumerate(aa):
                out[i + timeperiod - 1, j] = func(a, *args)
    elif arr.ndim == 2:
        for i, a in enumerate(arr):
            out[i + timeperiod - 1] = func(a, *args)

    return out


def numpy_rolling_apply(inputs, window, func1, func2, *args):
    """滚动应用方法 处理两个"""
    # 输出只与第一个的形状相同
    out = np.empty_like(inputs[0])
    fill_value = 0 if np.issubdtype(out.dtype, np.integer) else np.nan
    out[:window] = fill_value

    arrs = [np.lib.stride_tricks.sliding_window_view(i, window, axis=0) for i in inputs]

    return func1(*arrs, out, window, func2, *args)


def extend_shape(x, d, fill_value=np.nan):
    """扩展矩阵，在前部添加空值，用于sliding_window_view后还是保持形状"""
    shape = list(x.shape)
    shape[0] += d
    y = np.empty(shape=tuple(shape), dtype=x.dtype)
    y[:d] = fill_value
    y[d:] = x
    return y
