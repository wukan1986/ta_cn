import numba
import numpy as np

from .utils import pd_to_np


@numba.jit(nopython=True, cache=True, nogil=True)
def _rankdata_nb(a, pct=True):
    arr = np.ravel(a)

    nan_indexes = np.isnan(arr)
    sorter = np.argsort(arr)

    inv = np.empty(sorter.size, dtype=np.intp)
    inv[sorter] = np.arange(sorter.size, dtype=np.intp)

    if False:  # if method == 'ordinal':
        result = inv + 1

    if True:  # if method == 'average':
        arr = arr[sorter]
        # obs = np.r_[True, arr[1:] != arr[:-1]]
        obs = np.hstack((np.array([True]), arr[1:] != arr[:-1]))
        dense = obs.cumsum()[inv]

        # count = np.r_[np.nonzero(obs)[0], len(obs)]
        count = np.hstack((np.nonzero(obs)[0], np.array([len(obs)])))
        result = .5 * (count[dense] + count[dense - 1] + 1)

    result = result.astype('float64')
    result[nan_indexes] = np.nan

    if pct:
        return result / np.count_nonzero(arr == arr)
    else:
        return result


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
def _rolling_func_3_1_nb(arr0, arr1, arr2, out0, timeperiod, func, *args):
    """滚动函数，在二维或三维数上遍历，三组输入

    Parameters
    ----------
    arr0:
        输入。二维或三维
    out0:
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
                out0[i + timeperiod - 1, j] = func(a, b, c, *args)
    elif arr0.ndim == 2:
        for i, (a, b, c) in enumerate(zip(arr0, arr1, arr2)):
            out0[i + timeperiod - 1] = func(a, b, c, *args)

    return out0


@numba.jit(nopython=True, cache=True, nogil=True)
def _rolling_func_2_2_nb(arr0, arr1, out0, out1, timeperiod, func, *args):
    """滚动函数，在二维或三维数上遍历，二组输入

    Parameters
    ----------
    arr0:
        输入。二维或三维
    out0:
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
                out0[i + timeperiod - 1, j], out1[i + timeperiod - 1, j] = func(a, b, *args)
    elif arr0.ndim == 2:
        for i, (a, b) in enumerate(zip(arr0, arr1)):
            out0[i + timeperiod - 1], out1[i + timeperiod - 1] = func(a, b, *args)

    return out0, out1


@numba.jit(nopython=True, cache=True, nogil=True)
def _rolling_func_2_1_nb(arr0, arr1, out0, timeperiod, func, *args):
    """滚动函数，在二维或三维数上遍历，二组输入

    Parameters
    ----------
    arr0:
        输入。二维或三维
    out0:
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
                out0[i + timeperiod - 1, j] = func(a, b, *args)
    elif arr0.ndim == 2:
        for i, (a, b) in enumerate(zip(arr0, arr1)):
            out0[i + timeperiod - 1] = func(a, b, *args)

    return out0


@numba.jit(nopython=True, cache=True, nogil=True)
def _rolling_func_1_1_nb(arr0, out0, timeperiod, func, *args):
    """滚动函数，在二维或三维数上遍历，一组输入

    Parameters
    ----------
    arr0:
        输入。二维或三维
    out0:
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
        for i, aa in enumerate(arr0):
            for j, a in enumerate(aa):
                out0[i + timeperiod - 1, j] = func(a, *args)
    elif arr0.ndim == 2:
        for i, a in enumerate(arr0):
            out0[i + timeperiod - 1] = func(a, *args)

    return out0


def numpy_rolling_apply_1(inputs, window, func1, func2, *args):
    """滚动应用方法 处理两个"""
    # 输出只与第一个的形状相同
    out0 = np.empty_like(inputs[0])
    fill_value = 0 if np.issubdtype(out0.dtype, np.integer) else np.nan
    out0[:window] = fill_value

    if len(out0) < window:
        return out0

    arrs = [np.lib.stride_tricks.sliding_window_view(i, window, axis=0) for i in inputs]

    return func1(*arrs, out0, window, func2, *args)


def numpy_rolling_apply_2(inputs, window, func1, func2, *args):
    """滚动应用方法 处理两个"""
    # 输出只与第一个的形状相同
    out0 = np.empty_like(inputs[0])
    fill_value = 0 if np.issubdtype(out0.dtype, np.integer) else np.nan
    out0[:window] = fill_value

    out1 = out0.copy()

    if len(out0) < window:
        return out0, out1

    arrs = [np.lib.stride_tricks.sliding_window_view(i, window, axis=0) for i in inputs]

    return func1(*arrs, out0, out1, window, func2, *args)


def extend_shape(x, d, fill_value=np.nan):
    """扩展矩阵，在前部添加空值，用于sliding_window_view后还是保持形状"""
    shape = list(x.shape)
    shape[0] += d
    y = np.empty(shape=tuple(shape), dtype=x.dtype)
    y[:d] = fill_value
    y[d:] = x
    return y
