#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author     :wukan
# @License    :(C) Copyright 2022, wukan
# @Date       :2022-06-16
"""
Examples
--------
只要替换导入即可直接支持二维矩阵
>>> import talib as ta
>>> import ta_cn.talib as ta

"""
from functools import wraps

import numpy as np
import pandas as pd
import talib as _talib
from talib import abstract as _abstract


def tafunc_nditer_0(tafunc, args, kwargs, output_names):
    """直接调用talib"""
    return tafunc(*args, **kwargs)


def tafunc_nditer_1(tafunc, args, kwargs, output_names):
    """内部按列迭代函数，参数完全仿照talib

    Parameters
    ----------
    tafunc
        计算单列的函数
    args
        位置参数
    kwargs
        命名参数
    output_names: list
        tafunc输出参数名

    Returns
    -------
    tuple
        输出数组

    """

    def is_np_pd(x):
        """是否几种特数类型"""
        return isinstance(x, (pd.DataFrame, pd.DataFrame, np.ndarray))

    def pd_to_np(x):
        """pandas格式转numpy"""
        if isinstance(x, (pd.Series, pd.DataFrame)):
            return x.values
        return x

    # 分组
    args_input = [pd_to_np(v) for v in args if is_np_pd(v)]  # 位置非数字参数
    args_param = [pd_to_np(v) for v in args if not is_np_pd(v)]  # 位置数字参数
    kwargs_input = {k: pd_to_np(v) for k, v in kwargs.items() if is_np_pd(v)}  # 命名非数字参数
    kwargs_param = {k: pd_to_np(v) for k, v in kwargs.items() if not is_np_pd(v)}  # 命名数字参数

    # 取一个非数字，得用于得到形状
    if len(args_input) > 0:
        real = args_input[0]
    else:
        real = list(kwargs_input.values())[0]

    if real.ndim == 1:
        # 一维，直接计算并返回
        return tafunc(*args_input, *args_param, **kwargs_input, **kwargs_param)

    # =====以下是二维======

    # 输出缓存
    outputs = [np.empty_like(real) for _ in output_names]
    # 输入源
    inputs = [*args_input, *kwargs_input.values()]

    with np.nditer(inputs + outputs,
                   flags=['external_loop'], order='F',
                   op_flags=[['readonly']] * len(inputs) + [['writeonly']] * len(outputs)) as it:
        for in_out in it:
            _in = in_out[:len(inputs)]  # 分离输入
            args_in = in_out[:len(args_input)]  # 分离位置输入
            kwargs_in = {k: v for k, v in zip(kwargs_input.keys(), _in[len(args_input):])}  # 分离命名输入

            # 计算并封装
            ta_out = tafunc(*args_in, *args_param, **kwargs_in, **kwargs_param)
            if not isinstance(ta_out, tuple):
                ta_out = tuple([ta_out])

            # 转存数据
            _out = in_out[len(inputs):]  # 分离输出
            for _i, _o in zip(_out, ta_out):
                _i[...] = _o

    # 输出
    if len(outputs) == 1:
        return outputs[0]
    return outputs


def tafunc_nditer_2(tafunc, args, kwargs, output_names):
    """内部按列迭代函数，支持timeperiod等命名参数向量化

    Parameters
    ----------
    tafunc
        计算单列的函数
    args
        位置参数
    kwargs
        命名参数
    output_names: list
        tafunc输出参数名

    Returns
    -------
    tuple
        输出元组

    """

    def num_to_np(x, like):
        """将单字数字转成矩阵"""
        if hasattr(x, "__getitem__"):
            # 长度不足时，用最后一个值填充之后的参数
            y = np.full_like(like, fill_value=x[-1])
            # 长度超出时，截断
            y[:len(x)] = x[:len(y)]
            return y
        # 单一值，填充成唯一值
        return np.full_like(like, fill_value=x)

    real = args[0]

    if real.ndim == 1:
        # 一维，直接计算并返回
        return tafunc(*args, **kwargs)

    # =====以下是二维======

    # 输出缓存
    outputs = [np.empty_like(real) for _ in output_names]
    kwargs = {k: num_to_np(v, real[0]) for k, v in kwargs.items()}

    with np.nditer(list(args) + outputs,
                   flags=['external_loop'], order='F',
                   op_flags=[['readonly']] * len(args) + [['writeonly']] * len(outputs)) as it:
        for i, in_out in enumerate(it):
            _in = in_out[:-len(outputs)]  # 分离输入
            # 切片得到每列的参数
            _kw = {k: v[i] for k, v in kwargs.items()}

            # 计算并封装
            ta_out = tafunc(*_in, **_kw)
            if not isinstance(ta_out, tuple):
                ta_out = tuple([ta_out])

            _out = in_out[-len(outputs):]  # 分离输出
            for _i, _o in zip(_out, ta_out):
                _i[...] = _o

    # 输出
    if len(outputs) == 1:
        return outputs[0]
    return outputs


def ta_decorator(func, mode, output_names):
    # 设置对应处理函数
    ff = {0: tafunc_nditer_0, 1: tafunc_nditer_1, 2: tafunc_nditer_2}.get(mode)

    @wraps(func)
    def decorated(*args, **kwargs):
        return ff(func, args, kwargs, output_names)

    return decorated


def init(mode=1):
    """初始化环境

    Parameters
    ----------
    mode:
        0: 直接转向原版talib。只支持一维向量
        1: 输入数据支持二维矩阵。用法与原talib完全一样
        3. 输入参数支持一维向量。数据使用位置，周期等使用命名。否则报错

    """
    print(f'ta_cn 应用模式，当前为: {mode}')
    if mode == 0:
        print(f'\t0. 一维转发模式。直接转发的talib，因封装了一层，还失去了IDE智能提示，推荐直接使用原版talib')
    if mode == 1:
        print(f'\t1. 二维数据模式。既可以使用位置参数，也可以使用命名参数。与原talib完全一样。会根据类型自动区分是开高低收等数据，还是周期长度等参数')
    if mode == 2:
        print(f'\t2. 一维参数模式。在二维数据模式的基础上，周期参数由只支持标量升级为一维向量。命令参数用于传周期参数，位置参数用于传开高低收等数据，不可混淆。')

    for i, func_name in enumerate(_talib.get_functions()):
        """talib遍历"""
        _ta_func = getattr(_talib, func_name)
        output_names = _abstract.Function(func_name)._Function__info['output_names']

        # 创建函数
        globals()[func_name] = ta_decorator(_ta_func, mode, output_names)


# 默认使用二维矩阵模式
init(mode=1)
