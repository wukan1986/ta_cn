"""
长表处理工具
"""
from functools import wraps

import pandas as pd

from ta_cn.utils import to_pd


def series_groupby_apply(func, by, to_kwargs=[]):
    """普通指标转换成按分组处理的指标。只支持单参数

    Parameters
    ----------
    func
    by
    to_kwargs

    Notes
    -----
    只能处理Series

    """

    @wraps(func)
    def decorated(s: pd.Series, *args, **kwargs):
        # 参数位置调整，实现命命参数简化
        _kwargs = {k: args[i] for i, k in enumerate(to_kwargs)}

        return s.groupby(by=by, group_keys=False).apply(to_pd(func), **_kwargs, **kwargs)

    return decorated


def dataframe_groupby_apply(func, by, dropna, to_df=[], to_kwargs={}):
    """普通指标转换成按分组处理的指标。支持多输入

    Parameters
    ----------
    func
    by
    dropna
        慎用。丢弃后可能长度变小，与其它数据计算时长度不对
    to_df
    to_kwargs

    Notes
    -----
    即能处理DataFrame，又能处理Series,但考虑到效率，单输入时使用series_groupby_apply

    """

    def get(i, k, args, kwargs):
        if i == k:
            return args[i]
        if isinstance(k, str):
            v = kwargs.get(k, None)
            if v is None:
                return args[i]
            return v

    @wraps(func)
    def decorated(*args, **kwargs):
        df = pd.DataFrame({k: get(i, k, args, kwargs) for i, k in enumerate(to_df)})
        _kwargs = {k: args[i] for i, k in to_kwargs.items()}

        # 这里长度的变化会不会导致外部计算出错？
        if dropna:
            df = df.dropna()
        return df.groupby(by=by, group_keys=False).apply(to_pd(dataframe_split(func)), **_kwargs)

    return decorated


def dataframe_split(func):
    """将第一个DataFrame分拆传到指定函数"""

    @wraps(func)
    def decorated(df: pd.DataFrame, *args, **kwargs):
        ss = df.to_dict(orient='series')
        args_input = [v for k, v in ss.items() if isinstance(k, int)]
        kwargs_input = {k: v for k, v in ss.items() if not isinstance(k, int)}
        return func(*args_input, *args, **kwargs_input, **kwargs)

    return decorated