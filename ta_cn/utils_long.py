"""
长表处理工具
"""
from functools import wraps

import pandas as pd

from ta_cn.utils import to_pd


def series_groupby_apply(func, by='asset', to_kwargs=['timeperiod']):
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
    def decorated(s1: pd.Series, *args, **kwargs):
        # 参数位置调整，实现命命参数简化
        _kwargs = {k: args[i] for i, k in enumerate(to_kwargs)}

        # 跳过空值
        s2 = s1.dropna()
        if len(s2) == 0:
            return pd.Series(index=s1.index, dtype=float)

        s3 = s2.groupby(by=by, group_keys=False).apply(to_pd(func), **_kwargs, **kwargs)

        if len(s1) == len(s2):
            return s3
        else:
            # 由于长度变化了，只能重整长度
            return pd.Series(s3, index=s1.index)

    return decorated


def dataframe_groupby_apply(func, by='asset', to_kwargs={2: 'timeperiod'}, to_df=[0, 1], dropna=True):
    """普通指标转换成按分组处理的指标。支持多输入

    Parameters
    ----------
    func
    by
    dropna
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
        _kwargs = {k: args[i] for i, k in to_kwargs.items()}
        s1 = pd.DataFrame({k: get(i, k, args, kwargs) for i, k in enumerate(to_df)})
        if dropna:
            s2 = s1.dropna()
        else:
            s2 = s1
        if len(s2) == 0:
            return pd.Series(index=s1.index, dtype=float)

        s3 = s2.groupby(by=by, group_keys=False).apply(to_pd(dataframe_split(func)), **_kwargs)

        if len(s1) == len(s2):
            return s3
        else:
            # 由于长度变化了，只能重整长度
            return pd.Series(s3, index=s1.index)

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
