from typing import Union

import numpy as np
import pandas as pd


def num_to_np(x, like):
    """将单字数字转成矩阵

    Parameters
    ----------
    x: int or float
    like: array like

    """
    if isinstance(x, (pd.DataFrame, pd.Series, np.ndarray)):
        return x
    if not isinstance(like, (pd.DataFrame, pd.Series, np.ndarray)):
        return x
    return np.full_like(like, fill_value=x)


def np_to_pd(x: np.ndarray,
             copy: bool = False,
             index=None,
             columns=None) -> Union[pd.DataFrame, pd.Series]:
    """将ndarray类型的数据转化为Pandas中的Series或DataFrame

    Parameters
    ----------
    x: ndarray
        源数据
    copy: bool
        是否需要先建立副本
    index: pd.Index
        创建pd.DataFrame/pd.Series的index参数
    columns: pd.Index
        创建pd.DataFrame的columns参数

    Returns
    -------
    pd.DataFrame or pd.Series
        根据维数转换后DataFrame或Series类型的数据

    Examples
    --------
    >>> df = np_to_pd(arr, copy=False, index=close.index, columns=close.columns)

    """
    if copy:
        x = x.copy()
    if isinstance(x, np.ndarray):
        if x.ndim == 2:
            return pd.DataFrame(x, index=index, columns=columns)
        elif x.ndim == 1:
            return pd.Series(x, index=index)
        assert False
    return x


def pd_to_np(x: Union[pd.DataFrame, pd.Series], copy: bool = False) -> np.ndarray:
    """将Pandas中的Series、DataFrame类型数据转化为ndarray

    Parameters
    ----------
    x: pd.DataFrame or pd.Series
        需要进行转换的数据
    copy: bool
        是否需要先建立副本

    Returns
    -------
    ndarray
        转换后ndarray类型的数据

    Examples
    --------
    >>> arr = pd_to_np(df, copy=False)

    """
    if copy:
        x = x.copy()

    if isinstance(x, (pd.Series, pd.DataFrame)):
        return x.values

    return x


def fillna(arr, direction='down'):
    """numpy版fillna

    Parameters
    ----------
    arr: np.darray
    direction: str
        up, down, left, right

    Examples
    --------
    >>> arr = np.array([[5, np.nan, np.nan, 7, 2],
                [3, np.nan, 1, 8, np.nan],
                [np.nan, 9, 6, np.nan, np.nan],
                [2, np.nan, 6, 2, np.nan],])
    >>> fillna(arr, direction='down')

    References
    ----------
    https://stackoverflow.com/questions/41190852/most-efficient-way-to-forward-fill-nan-values-in-numpy-array

    """
    mask = np.isnan(arr)
    if direction == 'down':
        row = np.where(~mask, np.arange(mask.shape[0])[:, None], 0)
        np.maximum.accumulate(row, axis=0, out=row)
        out = arr[row, np.arange(row.shape[1])]
    if direction == 'up':
        row = np.where(~mask, np.arange(mask.shape[0])[:, None], mask.shape[0] - 1)
        row = np.minimum.accumulate(row[::-1, :], axis=0)[::-1, :]
        out = arr[row, np.arange(row.shape[1])]
    if direction == 'left':
        col = np.where(~mask, np.arange(mask.shape[1]), mask.shape[1] - 1)
        col = np.minimum.accumulate(col[:, ::-1], axis=1)[:, ::-1]
        out = arr[np.arange(col.shape[0])[:, None], col]
    if direction == 'right':
        col = np.where(~mask, np.arange(mask.shape[1]), 0)
        np.maximum.accumulate(col, axis=1, out=col)
        out = arr[np.arange(col.shape[0])[:, None], col]

    return out


def pushna(arr, direction='down'):
    """将非空数据按方向移动

    Parameters
    ----------
    arr: np.darray
    direction: str
        up, down, left, right

    Returns
    -------
    arr
        重排后的数据
    row
        行索引。将用于还原
    col
        列索引。将用于还原

    References
    ----------
    https://stackoverflow.com/questions/32062157/move-non-empty-cells-to-the-left-in-pandas-dataframe
    https://stackoverflow.com/questions/39361839/move-non-empty-cells-to-left-in-grouped-columns-pandas

    """
    if direction == 'down':
        row = (~np.isnan(arr)).argsort(axis=0, kind='stable')
        col = np.arange(arr.shape[1])[None]
    if direction == 'up':
        row = np.isnan(arr).argsort(axis=0, kind='stable')
        col = np.arange(arr.shape[1])[None]
    if direction == 'left':
        col = np.isnan(arr).argsort(axis=1, kind='stable')
        row = np.arange(arr.shape[0])[:, None]
    if direction == 'right':
        col = (~np.isnan(arr)).argsort(axis=1, kind='stable')
        row = np.arange(arr.shape[0])[:, None]

    return arr[row, col], row, col


def pullna(arr, row, col):
    """pushna的还原

    Parameters
    ----------
    arr: np.array
    row
        行索引
    col
        列索引

    Examples
    --------
    >>> a, row, col = pushna(df)
    >>> print(pullna(a, row, col))

    """
    tmp = np.empty_like(arr)
    tmp[row, col] = arr
    return tmp


def zero_runs(a):
    """查找0的边界

    Parameters
    ----------
    a

    Examples
    --------
    >>> a = [1, 2, 3, 0, 0, 0, 0, 0, 0, 4, 5, 6, 0, 0, 0, 0, 9, 8, 7, 0, 10, 11, 0]
    >>> zero_runs(a)

    References
    ----------
    https://stackoverflow.com/questions/24885092/finding-the-consecutive-zeros-in-a-numpy-array/

    """
    # Create an array that is 1 where a is 0, and pad each end with an extra 0.
    iszero = np.concatenate(([0], np.equal(a, 0).view(np.int8), [0]))
    absdiff = np.abs(np.diff(iszero))
    # Runs start and end where absdiff is 1.
    ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
    return ranges


def fill_zeros_with_last(arr):
    """0用上一个值填充，类似于ffill

    Parameters
    ----------
    arr

    Examples
    --------
    >>> arr = np.array([1, 0, 0, 8, 0, 4, 6, 2, 0, 0, 0, 0, 2])
    >>> fill_zeros_with_last(arr)

    References
    ----------
    https://stackoverflow.com/questions/30488961/fill-zero-values-of-1d-numpy-array-with-last-non-zero-values

    """
    prev = np.arange(len(arr))
    prev[arr == 0] = 0
    prev = np.maximum.accumulate(prev)
    return arr[prev]


if __name__ == '__main__':
    arr = np.array([[5, np.nan, np.nan, 7, 2],
                    [3, np.nan, 1, 8, np.nan],
                    [np.nan, 9, 6, np.nan, np.nan],
                    [2, np.nan, 6, 2, np.nan], ])
    print(fillna(arr, direction='down'))
    print(fillna(arr, direction='up'))
    print(fillna(arr, direction='left'))
    print(fillna(arr, direction='right'))

    print(pushna(arr, direction='down'))
    print(pushna(arr, direction='up'))
    print(pushna(arr, direction='left'))
    print(pushna(arr, direction='right'))
