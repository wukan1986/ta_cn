from functools import reduce

import numpy as np


def ABS(x):
    """绝对值"""
    return np.abs(x)


def LN(x):
    """底是e的对数"""
    return np.log(x)


def LOG(x):
    """底是10的对数"""
    return np.log10(x)


def POW(x1, x2):
    """次方"""
    return np.power(x1, x2)


def REVERSE(x):
    """相反数"""
    return -x


def SQRT(x):
    """平方根"""
    return np.sqrt(x)


def MAX(*args):
    """求max

    Examples
    --------
    >>> MAX(1, 2)
    >>> MAX(1, 2, 3)

    """
    return reduce(np.maximum, args)


def MIN(*args):
    """求min"""
    return reduce(np.minimum, args)


def ADD(*args):
    """求和

    Examples
    --------
    >>> ADD(1, 2)
    >>> ADD(1, 2, 3)

    """
    return reduce(np.add, args)


def SUB(*args):
    """相减"""
    return reduce(np.subtract, args)


def MUL(*args):
    """连乘"""
    return reduce(np.multiply, args)


def DIV(*args):
    """连除"""
    return reduce(np.true_divide, args)


def MEAN(*args):
    """均值"""
    return ADD(*args) / len(args)


def ROUND(a, decimals=3):
    """四舍五入取3位小数"""
    return np.round(a, decimals)


def SGN(x):
    """求符号方向

    np.sign对nan会报错，所以另实现了一版
    """
    return (0 < x) * 1 - (x < 0)
