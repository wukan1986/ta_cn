from functools import wraps, reduce
from typing import Union

import numpy as np
import pandas as pd


def to_pd(func):
    """将算子的numpy输出转成pandas的装饰器"""

    @wraps(func)
    def decorated(*args, **kwargs):
        real = args[0]
        return np_to_pd(func(*args, **kwargs),
                        index=getattr(real, 'index', None),
                        columns=getattr(real, 'columns', None))

    return decorated


def is_np_pd(x):
    """是否几种特数类型"""
    return isinstance(x, (pd.DataFrame, pd.Series, np.ndarray))


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


def ANY_NAN(*args):
    """多输入，同位置只要出现过nan就标记成True"""
    return reduce(lambda x, y: np.logical_or(x, np.isnan(y)), [False] + list(args))


def ALL_NOTNA(*args):
    """多输入，同位置没有出现过nan,标记成True"""
    return reduce(lambda x, y: np.logical_and(x, ~np.isnan(y)), [True] + list(args))


def round_a_i(func):
    """将参数 向量浮点 调整成 向量整数"""

    @wraps(func)
    def decorated(a, i):
        return func(a, round(i))

    return decorated


def round_a_a_i(func):
    """将参数 向量向量浮点 调整成 向量向量整数"""

    @wraps(func)
    def decorated(a, b, i):
        return func(a, b, round(i))

    return decorated


def dataframe_factorize(df, sort=False, na_sentinel=np.nan):
    """将DataFrame整体编码。比astype('category')版快

    Parameters
    ----------
    df: pd.DataFrame
    sort: bool
        按出现先后编码，还是按排序编码。astype('category')版自动排序
    na_sentinel: float or int
        NaN的处理方式。pandas内部是-1, 这里改成支持nan

    Returns
    -------
    codes: pd.Series or pd.DataFrame
        编码
    categories: pd.Index
        分类关系

    """

    if np.isnan(na_sentinel):
        codes, categories = pd.factorize(df.values.ravel(), sort=sort, na_sentinel=-1)
        codes = np.where(codes == -1, np.nan, codes)
    else:
        codes, categories = pd.factorize(df.values.ravel(), sort=sort, na_sentinel=na_sentinel)

    return np_to_pd(codes.reshape(df.shape), index=df.index, columns=df.columns), categories


def resample_agg(df, index_func='last', agg_func='last', rule='15min', **resample_kwarg):
    """对数据resample后再agg。时间标签来源于index，选择一周的最后一个交易日，而不是周日

    Parameters
    ----------
    df
    index_func: str or None
        索引标签处理方法。None表示按resample_kwarg中的label设置
    agg_func: str or dict
        聚合函数
    rule: str
        采样规则
    resample_kwarg
        resample参数

    Notes
    -----
    如果所有数据都是resample过后的，就算对齐时那天不是交易日也没关系，不影响结果

    Examples
    --------
    >>> resample_agg(df, agg_func='sum', index_func='last', rule='W')
    >>> resample_agg(df['IC9999.CCFX'], agg_func='sum', index_func='first', rule='W')
    >>> resample_agg(df, index_func='last', agg_func='sum', rule='15min', closed='right')
    >>> resample_agg(df, index_func=None, agg_func='sum', rule='8h', offset='4h', closed='right')

    """
    assert index_func in ('first', 'last', None)

    dt = pd.Series(df.index, index=df.index)
    if index_func is None:
        # 对时间进行resample
        dt = dt.resample(rule, **resample_kwarg).agg('first')
        df = df.resample(rule, **resample_kwarg).agg(agg_func)
        # 删除resample出现的NaT
        return df.loc[dt.notna()]
    else:
        dt = dt.resample(rule, **resample_kwarg).agg(index_func)
        df = df.resample(rule, **resample_kwarg).agg(agg_func)
        df.index = dt
        # 删除resample出现的NaT
        return df.loc[df.index.notna()]


def resample_agg_1d(df, index_func='last', agg_func='sum', groupby_agg_func='sum', floor_date=False, **resample_kwarg):
    """resample得到日线数据

    Parameters
    ----------
    df
    index_func
    agg_func
    groupby_agg_func: str
        分组合并方法。周六至周一将合并，不同的数据合并方法不一样。例如:
            - open: first
            - volume: sum
            - low: min
            - close: last
    floor_date: bool
        是否调整index将时间去除只保留日期
    resample_kwarg

    Examples
    --------
    >>> resample_agg_1d(df, index_func='last', agg_func='sum', groupby_agg_func='sum', floor_date=True, closed='right')

    """
    df_1d = resample_agg(df, index_func=index_func, agg_func=agg_func, rule='1d', offset='20h', **resample_kwarg)
    # resample时间用的first也会移动到第二天
    t = df_1d.index + pd.Timedelta(hours=4)
    df_1d['_date_'] = t

    # 周六日需要移动到下周一
    is_w6_w7 = t.weekday >= 5

    df_1d.loc[is_w6_w7, '_date_'] = pd.NaT
    # return df_1d
    df_1d['_date_'].bfill(inplace=True)

    df_1d = df_1d.groupby(by='_date_').agg(groupby_agg_func)
    # 时间还原
    df_1d.index -= pd.Timedelta(hours=4)
    # return df_1d
    if floor_date:
        df_1d.index = pd.to_datetime(df_1d.index.date)
    return df_1d
