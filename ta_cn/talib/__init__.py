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
import talib as _talib
from talib import abstract as _abstract

from ..utils import ANY_NAN, ALL_NOTNA


def tafunc_nditer_1(tafunc, args, kwargs, output_names, skipna):
    """直接调用talib"""
    # 不跳过空值，直接调用函数
    if not skipna:
        return tafunc(*args, **kwargs)

    # 取一个非数字，得用于得到形状
    real = args[0]

    # 输出缓存
    outputs = [np.full_like(real, fill_value=np.nan) for _ in output_names]

    _notna = ALL_NOTNA(*args)
    for i in range(1):
        _in = [v[_notna] for v in args]

        # 全NaN，跳过
        if len(_in[0]) == 0:
            continue

        # 计算并封装
        ta_out = tafunc(*_in, **kwargs)
        if not isinstance(ta_out, tuple):
            ta_out = tuple([ta_out])

        for _i, _o in zip(outputs, ta_out):
            _i[_notna] = _o

    # 输出
    if len(outputs) == 1:
        return outputs[0]
    return outputs


def tafunc_nditer_2(tafunc, args, kwargs, output_names, skipna):
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
        return tafunc_nditer_1(tafunc, args, kwargs, output_names, skipna)

    # =====以下是二维======
    inputs = [*args]

    # 输出缓存
    outputs = [np.full_like(real, fill_value=np.nan) for _ in output_names]
    if skipna:
        notna = ALL_NOTNA(*args)
    else:
        notna = np.ones_like(real, dtype=bool)

    kwargs = {k: num_to_np(v, real[0]) for k, v in kwargs.items()}

    # 只有一行输入时需要特别处理
    with np.nditer(inputs + [notna] + outputs,
                   flags=['external_loop'] if real.shape[0] > 1 else None,
                   order='F',
                   op_flags=[['readonly']] * (len(inputs) + 1) + [['writeonly']] * len(outputs)) as it:
        for i, in_out in enumerate(it):
            if real.shape[0] == 1:
                # 需要将0维array改成1维，否则talib报错
                in_out = [v.reshape(1) for v in in_out]

            _in = in_out[:len(inputs)]  # 分离输入
            _notna = in_out[len(inputs)]
            _out = in_out[-len(outputs):]  # 分离输出
            # 切片得到每列的参数
            _kw = {k: v[i] for k, v in kwargs.items()}

            if skipna:
                _in = [v[_notna] for v in _in]

                # 全NaN，跳过
                if len(_in[0]) == 0:
                    continue
            else:
                _notna = slice(None)
                # 所有输入数据都判断一下
                if np.all(ANY_NAN(*_in)):
                    continue

            # 计算并封装
            ta_out = tafunc(*_in, **_kw)
            if not isinstance(ta_out, tuple):
                ta_out = tuple([ta_out])

            for _i, _o in zip(_out, ta_out):
                _i[_notna] = _o

    # 输出
    if len(outputs) == 1:
        return outputs[0]
    return outputs


def ta_decorator(func, mode, output_names, skipnan):
    # 设置对应处理函数
    ff = {1: tafunc_nditer_1, 2: tafunc_nditer_2}.get(mode)

    @wraps(func)
    def decorated(*args, **kwargs):
        return ff(func, args, kwargs, output_names, skipnan)

    return decorated


def init(mode=1, skipna=False):
    """初始化环境

    Parameters
    ----------
    mode: int
        1: 输入数据支持一维矩阵。数据使用位置，周期等使用命名
        2. 输入参数支持一维向量。数据使用位置，周期等使用命名。否则报错
    skipna: bool
        是否跳过空值。跳过空值功能会导致计算变慢。
        - 确信数据不会中途出现空值建议设置成False, 加快计算（如pushna后的数据）

    """
    print(f'ta_cn mode: {mode}, skipna: {skipna}')
    assert mode in (1, 2)
    if mode == 1:
        print(f'\t1. 输入一维数据，支持skipna跳过空值。必须使用命名参数传入周期，使用位置参数传入数据。')
    if mode == 2:
        print(f'\t2. 输入二维数据，支持skipna跳过空值。必须使用命名参数传入周期，使用位置参数传入数据。周期参数由只支持标量升级为一维向量')

    for i, func_name in enumerate(_talib.get_functions()):
        """talib遍历"""
        _ta_func = getattr(_talib, func_name)
        output_names = _abstract.Function(func_name)._Function__info['output_names']

        # 创建函数
        globals()[func_name] = ta_decorator(_ta_func, mode, output_names, skipna)


# =============================================

TA_COMPATIBILITY_DEFAULT = 0  # 使用MA做第一个值
TA_COMPATIBILITY_METASTOCK = 1  # 使用Price做第一个值

_COMPATIBILITY_ENABLE_ = False


def set_compatibility_enable(enable):
    """talib兼容性设置"""
    global _COMPATIBILITY_ENABLE_
    _COMPATIBILITY_ENABLE_ = enable


def set_compatibility(compatibility):
    """talib兼容性设置"""
    global _COMPATIBILITY_ENABLE_
    if _COMPATIBILITY_ENABLE_:
        print('do talib.set_compatibility', compatibility)
        _talib.set_compatibility(compatibility)
