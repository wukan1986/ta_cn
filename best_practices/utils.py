"""
文件分组处理相关
"""
import os
import pathlib
from typing import Union, List, Tuple, Dict, Any

import pandas as pd
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
            df = df.groupby(by=groupby).apply(func)

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
            columns = list(set(include) | set([AXIS_I, AXIS_J]))
            _df = df[columns]
        elif exclude:
            columns = list(set(df.columns) - set(exclude) | set([AXIS_I, AXIS_J]))
            _df = df[columns]
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
        df.to_parquet(path / name, compression='gzip')
    elif split_axis == 1:
        # 整列拆分成多行
        for key, group in df.groupby(by=AXIS_J):
            group.to_parquet(path / f'{i}__{key:02d}.parquet', compression='gzip')
    else:
        # 整行拆分成多列
        for key, group in df.groupby(by=AXIS_I):
            group.to_parquet(path / f'{key:02d}__{j}.parquet', compression='gzip')


def load_parquet_index(path: Union[str, pathlib.Path], pattern: Union[str, List[str]], columns=None):
    """根据文件名模式（非正则表达式）。加载多个parquet文件，纵向合并

    Parameters
    ----------
    path: str
        目录
    pattern: str or list
        模式。如果是列表，将依次加载合并
    columns: list
        指定要加载的列。按需加载可以减少内存占用

    Returns
    -------
    pd.DataFrame

    Examples
    --------
    >>> load_parquet_index(path, f'{year}*', columns=None)

    """
    if isinstance(pattern, str):
        # 一个过滤条件时，拼接一组
        return pd.concat([pd.read_parquet(_, columns=columns) for _ in pathlib.Path(path).glob(pattern)])
    if isinstance(pattern, list):
        # 多个过滤条件时，拼接多组
        return pd.concat([load_parquet_index(path, _, columns=columns) for _ in pattern])


def load_parquet_column(path: Union[str, pathlib.Path], pattern: Union[str, List[str]], columns=None):
    """根据文件名模式（非正则表达式）。加载多个parquet文件，横向合并

    Parameters
    ----------
    path: str
        目录
    pattern: str or list
        模式。支持?*通配符。如果是列表，将依次加载合并
    columns: list
        指定要加载的列。按需加载可以减少内存占用

    Returns
    -------
    pd.DataFrame

    Notes
    -----
    需要有相同的索引，否则合并错误

    """
    if isinstance(pattern, str):
        # 一个过滤条件时，拼接一组
        return pd.concat([pd.read_parquet(_, columns=columns) for _ in pathlib.Path(path).glob(pattern)], axis=1)
    if isinstance(pattern, list):
        # 多个过滤条件时，拼接多组
        return pd.concat([load_parquet_column(path, _, columns=columns) for _ in pattern], axis=1)


def load_parquet_two(left_path, right_path,
                     left_pattern, right_pattern,
                     **merge_kwargs):
    """加载两组文件，并横向合并

    Parameters
    ----------
    left_path:
    right_path
    left_pattern
    right_pattern
    merge_kwargs:
        pd.merge的参数

    Returns
    -------
    pd.DataFrame

    """
    df_left = load_parquet_index(left_path, left_pattern)
    df_right = load_parquet_index(right_path, right_pattern)
    return pd.merge(df_left, df_right, how='left', suffixes=('', '_DROP'), **merge_kwargs).filter(regex='^(?!.*_DROP)')


def func_load_index_column(i, j,
                           left_path, right_path,
                           left_pattern, right_pattern,
                           left_on, right_on):
    """加载两路径下的数据，先纵向合并，再横向合并

    Parameters
    ----------
    i
    j
    left_path
    right_path
    left_pattern
    right_pattern
    left_on
    right_on

    Returns
    -------

    """
    return load_parquet_two(left_path, right_path,
                            left_pattern.format(i, j), right_pattern.format(i, j),
                            left_on=left_on, right_on=right_on)


def func_load_index(i, j, path, columns=None):
    """加载路径下的数据，并纵向合并

    Parameters
    ----------
    i:
        行信息
    j:
        列信息
    path
        路径
    columns
        指定列名

    Returns
    -------
    pd.DataFrame

    """
    return load_parquet_index(path, f'{i}__{j}.parquet', columns)