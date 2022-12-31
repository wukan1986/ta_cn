"""
文件分组处理相关
"""
import os
import pathlib
import time
from functools import wraps
from typing import Union, List, Tuple, Dict, Any

import pandas as pd
import polars as pl
from loguru import logger

AXIS_I = 'axis_0'
AXIS_J = 'axis_1'


#########
# 计算函数
#########
def dataframe_calc(df: pd.DataFrame, i, j, *args):
    """dataframe计算

    1. 如果指标体系可以计算长表，那就没有必要走这一步
    2. 如果要计算多个指标，统一groupby会更快

    Parameters
    ----------
    df: pd.DataFrame
        复合索引的数据
    i,j:
        行列坐标
    args: list
        groupby
            处理方向，None表示不用groupby,直接操作
            1. 直接None，本质是直接调用函数处理整个数据区
            2. 非None,本质是对分组后的各小段Series进行apply
        func
            不分组，直接处理。如一列与另一列的处理
            分组，组内进行计算，比如算指标，算排序等

    Notes
    -----
    !!! 输入数据非常重要
    1. 时序数据可以按年按月分段，然后并行计算。但不能分太多，否则长度过短计算也慢
    2. 横截面计算必需数据同时存在
        1. 不做横截面切片，所有股票放一个文件
        2. 做了切片，但计算但横截面计算很靠后，所以在最后一步之前做一次合并

    Returns
    -------
    pd.DataFrame

    """
    for arg in args:
        groupby = arg.get('groupby', None)
        func = arg.get('func')
        if groupby is None:
            # 不分组，对整个数据进行操作
            df = func(df)
        else:
            # 注意分组方向
            df = df.groupby(by=groupby, group_keys=False).apply(func)

    return df


def dataframe_save(df: pd.DataFrame, i, j, *args):
    """dataframe保存。实现了多输出功能

    除了一般的全保存外，还有特别的用法。即指定部分列进行保存。有了它可以将数据分别保存到不同的目录，比如需要横截面计算的数据另外保存

    Parameters
    ----------
    df:
    i,j:
        行列坐标
    args: list
        split_axis
        path
        exclude/include

    """
    for arg in args:
        split_axis = arg.get('split_axis', None)
        path = arg.get('path', None)
        exclude = arg.get('exclude', [])
        include = arg.get('include', [])
        if include:
            _df = df[include]
        elif exclude:
            _df = df.drop(columns=exclude)
        else:
            _df = df

        save_parquet(_df, i, j, path=path, split_axis=split_axis)


#######
# 核心块
#######
def func_load_calc_save(ij: List[Tuple],
                        load_func=None, load_kwargs: Dict[str, Any] = {},
                        calc_func=None, calc_args: List[Any] = [],
                        save_func=None, save_args: List[Any] = []):
    """单进程任务

    Parameters
    ----------
    ij:tuple
        行号，列号
    load_func
        输入函数
    load_kwargs
        输入参数
    calc_func
        计算函数
    calc_args
        计算参数
    save_func
        保存函数
    save_args
        保存参数

    """
    logger.info('pid:{}, ij:{}', os.getpid(), ij)

    # 加载
    df = load_func(*ij, **load_kwargs)

    if calc_func:
        # 计算
        df = calc_func(df, *ij, *calc_args)

    # 保存
    save_func(df, *ij, *save_args)

    # 释放内存
    del df


def save_parquet(df, i, j, path, split_axis):
    """保存

    Parameters
    ----------
    df:
        数据
    i:
        行信息
    j:
        列信息
    path:
        路径
    split_axis:
        分割文件所用的轴
        None，不分割，按输入数据直接保存
        0，行方向分割
        1，列方向分割

    """

    path = pathlib.Path(path)
    path.mkdir(parents=True, exist_ok=True)

    if split_axis is None:
        # 输入和输出同方向，整行或整列保存
        name = f'{i}__{j}.parquet'.replace('*', 'X')
        df.to_parquet(path / name, compression='zstd')
    elif split_axis == 1:
        # 整列拆分成多行
        for key, group in df.groupby(by=AXIS_J):
            group.to_parquet(path / f'{i}__{key:02d}.parquet', compression='zstd')
    else:
        # 整行拆分成多列
        for key, group in df.groupby(by=AXIS_I):
            group.to_parquet(path / f'{key:02d}__{j}.parquet', compression='zstd')


def load_parquet(path: Union[str, pathlib.Path], pattern: Union[str, List[str]], axis, columns=None, func=None):
    """根据文件名模式（非正则表达式）。加载多个parquet文件，必须同结构

    Parameters
    ----------
    path: str
        目录
    pattern: str or list
        模式。支持?*通配符。如果是列表，将依次加载合并
    axis:
        concat合并方向
    columns: list
        指定要加载的列。按需加载可以减少内存占用
    func

    Returns
    -------
    pd.DataFrame

    Notes
    -----
    需要有相同的索引，否则合并错误

    """
    if func is None:
        func = lambda x: x

    if isinstance(pattern, str):
        # 一个过滤条件时，拼接一组
        return pd.concat([func(pd.read_parquet(_, columns=columns)) for _ in pathlib.Path(path).glob(pattern)],
                         axis=axis)
    if isinstance(pattern, list):
        # 多个过滤条件时，拼接多组
        return pd.concat([load_parquet(path, _, columns=columns) for _ in pattern], axis=axis)


def func_load_parquet(i, j,
                      path=[],
                      pattern=[],
                      axis=[],
                      func=[],
                      on=[],
                      index=[]):
    """加载两路径下的数据，先纵向合并，再横向合并

    Parameters
    ----------
    i
    j
    path
    pattern
    axis
    func
    on
    index

    Returns
    -------

    """
    dfs = []
    for k in range(len(path)):
        df = load_parquet(path[k], pattern[k].format(i, j), axis=axis[k], func=None)
        f = func[k]
        if f is not None:
            df = f(df)
        dfs.append(df)

    left = dfs[0]
    left_on = on[0]
    left_index = index[0]
    for k in range(1, len(dfs)):
        right = dfs[k]
        right_on = on[k]
        right_index = index[k]
        left = pd.merge(left, right, how='left', suffixes=('', '_DROP'),
                        left_on=left_on, right_on=right_on,
                        left_index=left_index, right_index=right_index,
                        ).filter(regex='^(?!.*_DROP)')
    return left


def describe_win(df: pd.DataFrame):
    """统计胜率"""
    desc = df.describe()
    # 为正的概率，False为亏，True为挣
    counts = (df > 0).apply(pd.value_counts)
    x = counts / counts.sum(axis=0)
    y = pd.concat([counts.tail(1), x.tail(1)])
    y.index = ['win_count', 'win_ratio']
    return pd.concat([desc, y])


def timer(func):
    """timer装饰器"""

    @wraps(func)
    def wrap(*args, **kwargs):
        begin_time = time.perf_counter()
        logger.info('Start call func:%r args:[%r, %r]' % (func.__name__, args, kwargs))
        result = func(*args, **kwargs)
        start_time = time.perf_counter()
        logger.info(
            'End call func:%r args:[%r, %r] took: %2.4f sec' % (func.__name__, args, kwargs, start_time - begin_time))
        return result

    return wrap


def pl_np_wraps(func, in_num: int = 1, out_num: int = 1, dtype=pl.Float32):
    """普通函数包装，将输入由Series转成numpy，将输出由numpy转回Series

    Parameters
    ----------
    func:
        需要封装的函数
    in_num:int
        入参需要转numpy的数量
    out_num:int
        出参需要转Series的数量
    dtype:
        返回前，指定数据类型，可减少内存占用

    Notes
    -----
    TA-Lib 0.4.24 开始已经支持polars, 可以不套用此装饰器

    """

    @wraps(func)
    def decorated(*args, **kwargs):
        args_left = (_.to_numpy() for _ in args[:in_num])
        args_right = args[in_num:]

        outs = func(*args_left, *args_right, **kwargs)
        if out_num == 1:
            return pl.Series(outs, dtype=dtype)
        else:
            return tuple(pl.Series(_, dtype=dtype) for _ in outs)

    return decorated
