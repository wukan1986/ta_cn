import numba
import numpy as np

from .utils import pd_to_np


@numba.jit(nopython=True, cache=True)
def _FILTER_1d_nb(arr, n):
    """内部函数，请勿直接调用，请参考"""
    i = 0
    while i < len(arr):
        if arr[i]:
            arr[i + 1:i + 1 + n] = 0
            i += n + 1
    return arr


@numba.jit(nopython=True, cache=True)
def _FILTER_2d_nb(arr, n):
    """内部函数，请勿直接调用"""
    for j in range(arr.shape[1]):
        i = 0
        while i < len(arr):
            if arr[i, j]:
                arr[i + 1:i + 1 + n, j] = 0
                i += n + 1
    return arr


@numba.jit(nopython=True, cache=True)
def _fill_notna_1d_nb(arr, fill_value, n: int):
    k = n
    for i in range(len(arr)):
        if np.isnan(arr[i]):
            continue
        arr[i] = fill_value
        k -= 1
        if k <= 0:
            break


@numba.jit(nopython=True, cache=True)
def _fill_notna_2d_nb(arr, fill_value, n: int):
    for i in range(arr.shape[1]):
        k = n
        for j in range(arr.shape[0]):
            if np.isnan(arr[j, i]):
                continue
            arr[j, i] = fill_value
            k -= 1
            if k <= 0:
                break


def fill_notna(arr, fill_value, n=1):
    """查找第一个非nan,将其改成fill_value"""
    if n < 1:
        return arr
    arr = pd_to_np(arr, copy=True)
    if arr.ndim == 2:
        _fill_notna_2d_nb(arr, fill_value, n)
    else:
        _fill_notna_1d_nb(arr, fill_value, n)
    return arr
