"""
长表处理工具
"""
from functools import wraps

import pandas as pd

from .utils import to_pd


def series_groupby_apply(func, by='asset', dropna=True, to_kwargs={1: 'timeperiod'}, output_num=1):
    """普通指标转换成按分组处理的指标。只支持单参数

    Parameters
    ----------
    func
    by
    dropna
    to_kwargs
    output_num

    Notes
    -----
    只能处理Series

    """

    @wraps(func)
    def decorated(*args, **kwargs):
        # 参数位置调整，实现命命参数简化
        _kwargs = {k: args[i] for i, k in to_kwargs.items() if i < len(args)}
        s1 = args[0]

        if dropna:
            s2 = s1.dropna()
        else:
            s2 = s1

        if len(s2) == 0:
            if output_num == 1:
                return pd.Series(index=s1.index, dtype=float)
            else:
                return tuple([pd.Series(index=s1.index, dtype=float) for i in range(output_num)])

        s3 = s2.groupby(by=by, group_keys=False).apply(to_pd(func), **_kwargs, **kwargs)

        if output_num == 1:
            # 单输出
            if len(s1) == len(s2):
                return s3
            else:
                # 由于长度变化了，只能重整长度
                return pd.Series(s3, index=s1.index)
        else:
            # 多输出
            return tuple([pd.concat([s[i] for s in s3]) for i in range(output_num)])

    return decorated


def dataframe_groupby_apply(func, by='asset', dropna=True, to_df=[0, 1], to_kwargs={2: 'timeperiod'}, output_num=1):
    """普通指标转换成按分组处理的指标。支持多输入

    Parameters
    ----------
    func
    by
    dropna
    to_df
    to_kwargs
    output_num

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
        _kwargs = {k: args[i] for i, k in to_kwargs.items() if i < len(args)}
        s1 = pd.DataFrame({k: get(i, k, args, kwargs) for i, k in enumerate(to_df)})

        if dropna:
            s2 = s1.dropna()
        else:
            s2 = s1

        if len(s2) == 0:
            if output_num == 1:
                return pd.Series(index=s1.index, dtype=float)
            else:
                return tuple([pd.Series(index=s1.index, dtype=float) for i in range(output_num)])

        s3 = s2.groupby(by=by, group_keys=False).apply(to_pd(dataframe_split(func)), **_kwargs)

        if output_num == 1:
            # 单输出
            if len(s1) == len(s2):
                return s3
            else:
                # 由于长度变化了，只能重整长度
                return pd.Series(s3, index=s1.index)
        else:
            # 多输出
            return tuple([pd.concat([s[i] for s in s3]) for i in range(output_num)])

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
