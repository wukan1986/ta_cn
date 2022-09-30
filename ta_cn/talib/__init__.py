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
>>> _ta1d = ta.init(mode=1, skipna=False, to_globals=False)
>>> _ta2d = ta.init(mode=2, skipna=False, to_globals=False)

"""
from functools import wraps, reduce

import numpy as np
import talib as _talib
from talib import abstract as _abstract


def tafunc_nditer_1(tafunc, args, kwargs, input_names, output_names, skipna):
    """直接调用talib"""

    def ALL_NOTNA(*args):
        """多输入，同位置没有出现过nan,标记成True"""
        return reduce(lambda x, y: np.logical_and(x, ~np.isnan(y)), [True] + list(args))

    # 不跳过空值，直接调用函数
    if not skipna:
        return tafunc(*args, **kwargs)

    # 取一个非数字，得用于得到形状
    real = args[0]

    output_num = len(output_names)

    outputs = [np.full_like(real, fill_value=np.nan) for _ in output_names]

    _notna = ALL_NOTNA(*args)
    # 只有不连续的nan才需要做切片 https://www.cnpython.com/qa/352363
    # TODO: https://stackoverflow.com/questions/41721674/find-consecutive-repeated-nan-in-a-numpy-array/41722059#41722059
    _in = [v[_notna] for v in args]

    if len(_in[0]) > 0:
        ta_out = tafunc(*_in, **kwargs)
        if output_num == 1:
            ta_out = [ta_out]

        for _i, _o in zip(outputs, ta_out):
            _i[_notna] = _o

    # 输出
    return outputs[0] if output_num == 1 else tuple(outputs)


def tafunc_nditer_2(tafunc, args, kwargs, input_names, output_names,
                    skipna, order='F'):
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
    skipna:
        如想跳过空值，需将数据堆叠到首或尾，实现连续计算
    order:
        F, 按列进行遍历
        C, 按行进行遍历

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

    def last_isna(x):
        # 只检查最后一行
        return np.any([y[-1] != y[-1] for y in x])

    real = args[0]

    if real.ndim == 1:
        return tafunc_nditer_1(tafunc, args, kwargs, input_names, output_names, skipna)

    # =====以下是二维======
    inputs = [*args]

    # 输出缓存
    outputs = [np.full_like(real, fill_value=np.nan) for _ in output_names]
    kwargs = {k: num_to_np(v, real[0]) for k, v in kwargs.items()}

    # 只有一行输入时需要特别处理
    with np.nditer(inputs + outputs,
                   flags=['external_loop'] if real.shape[0] > 1 else None,
                   order=order,
                   op_flags=[['readonly']] * len(inputs) + [['writeonly']] * len(outputs)) as it:
        for i, in_out in enumerate(it):
            if real.shape[0] == 1:
                # 需要将0维array改成1维，否则talib报错
                in_out = [v.reshape(1) for v in in_out]

            _in = in_out[:len(inputs)]  # 分离输入
            # 最后一行出现了空
            if last_isna(_in):
                continue
            _out = in_out[-len(outputs):]  # 分离输出

            # 切片得到每列的参数
            _kw = {k: v[i] for k, v in kwargs.items()}

            # 计算并封装
            ta_out = tafunc(*_in, **_kw)
            if not isinstance(ta_out, tuple):
                ta_out = tuple([ta_out])

            for _i, _o in zip(_out, ta_out):
                _i[...] = _o

    # 输出
    if len(outputs) == 1:
        return outputs[0]
    return outputs


def ta_decorator(func, mode, input_names, output_names, skipnan):
    # 设置对应处理函数
    ff = {1: tafunc_nditer_1, 2: tafunc_nditer_2}.get(mode)

    @wraps(func)
    def decorated(*args, **kwargs):
        return ff(func, args, kwargs, input_names, output_names, skipnan)

    return decorated


def init(mode=1, skipna=False, to_globals=False):
    """初始化环境

    Parameters
    ----------
    mode: int
        1: 输入数据支持一维矩阵。数据使用位置，周期等使用命名
        2. 输入参数支持一维向量。数据使用位置，周期等使用命名。否则报错
    skipna: bool
        是否跳过空值。跳过空值功能会导致计算变慢。
        - 确信数据不会中途出现空值建议设置成False, 加快计算
    to_globals: bool
        注册到包中

    """
    assert mode in (1, 2)

    class TA_CN_LIB:
        pass

    lib = TA_CN_LIB()
    for i, func_name in enumerate(_talib.get_functions()):
        """talib遍历"""
        _ta_func = getattr(_talib, func_name)
        info = _abstract.Function(func_name).info
        output_names = info['output_names']
        input_names = info['input_names']

        # 创建函数
        f = ta_decorator(_ta_func, mode, input_names, output_names, skipna)
        setattr(lib, func_name, f)
        if to_globals:
            globals()[func_name] = f

    return lib


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
