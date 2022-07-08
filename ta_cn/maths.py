from functools import reduce

import numpy as _np


def ABS(x):
    """绝对值"""
    return _np.abs(x)


def LN(x):
    """底是e的对数

    0返回-inf。不好看，还是先用where过滤
    """
    return _np.log(_np.where(x > 0, x, _np.nan))


def LOG(x):
    """底是10的对数"""
    return _np.log10(_np.where(x > 0, x, _np.nan))


def POW(x1, x2):
    """次方"""
    return _np.power(x1, x2)


def REVERSE(x):
    """相反数"""
    return -x


def SQRT(x):
    """平方根"""
    with _np.errstate(invalid='ignore'):
        return _np.sqrt(x)


def MAX(*args):
    """求max

    Examples
    --------
    >>> MAX(1, 2)
    >>> MAX(1, 2, 3)

    """
    return reduce(_np.maximum, args)


def MIN(*args):
    """求min"""
    return reduce(_np.minimum, args)


def ADD(*args):
    """求和

    Examples
    --------
    >>> ADD(1, 2)
    >>> ADD(1, 2, 3)

    """
    return reduce(_np.add, args)


def SUB(*args):
    """相减"""
    return reduce(_np.subtract, args)


def MUL(*args):
    """连乘"""
    return reduce(_np.multiply, args)


def DIV(*args):
    """连除

    RuntimeWarning: invalid value encountered in true_divide
    """
    with _np.errstate(divide='ignore', invalid='ignore'):
        return reduce(_np.true_divide, args)


def MEAN(*args):
    """均值"""
    return ADD(*args) / len(args)


def ROUND(a, decimals=3):
    """四舍五入取3位小数"""
    return _np.round(a, decimals)


def SGN(x):
    """求符号方向

    return (0 < x) * 1 - (x < 0)
    """
    return _np.sign(x)


if __name__ == '__main__':
    a = _np.random.rand(10000)
    a[:20] = _np.nan
    a[:10] = -10
    a[:5] = 0
    b = ABS(a)
    print(b)
    b = LN(a)
    print(b)
    b = LOG(a)
    print(b)
    b = SQRT(a)
    print(b)
    b = DIV(a, a)
    print(b)
    b = SGN(a)
    print(b)
