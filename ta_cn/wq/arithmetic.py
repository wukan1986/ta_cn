"""
Arithmetic Operators
"""
from functools import reduce

import numpy as np

from .time_series import ts_delta


def abs(x):
    """Absolute value of x"""
    return np.absolute(x)


def add(*args, filter=False):
    """Add all inputs (at least 2 inputs required). If filter = true, filter all input NaN to 0 before adding"""

    def _add(x, y):
        x = np.nan_to_num(x, nan=0)
        y = np.nan_to_num(y, nan=0)
        x = np.ma.masked_array(x, mask=np.isnan(x) & np.isnan(y))
        y = np.ma.masked_array(y, mask=x.mask)
        return (x + y).filled(np.nan)

    func = _add if filter else np.add

    with np.errstate(over='ignore'):
        return reduce(func, args)


def ceiling(x):
    """Nearest larger integer"""
    return np.ceil(x)


def divide(*args):
    """x / y"""
    with np.errstate(divide='ignore', invalid='ignore'):
        return reduce(np.true_divide, args)


def exp(x):
    """Natural exponential function: e^x"""
    return np.exp(x)


def floor(x):
    """Nearest smaller integer"""
    return np.floor(x)


def fraction(x):
    """This operator removes the whole number part and returns the remaining fraction part with sign."""
    return sign(x) * (abs(x) - floor(abs(x)))


def inverse(x):
    """1 / x"""
    x = x.copy()
    x[x == 0] = np.nan
    return 1 / x


def log(x):
    """Natural logarithm. For example: Log(high/low) uses natural logarithm of high/low ratio as stock weights."""
    return np.log(np.where(x > 0, x, np.nan))


def log_diff(x):
    """Returns log(current value of input or x[t] ) - log(previous value of input or x[t-1])."""
    return ts_delta(log(x), 1)


def max(*args):
    """Maximum value of all inputs. At least 2 inputs are required."""
    return reduce(np.maximum, args)


def min(*args):
    """Minimum value of all inputs. At least 2 inputs are required."""
    return reduce(np.minimum, args)


def multiply(*args, filter=False):
    """Multiply all inputs. At least 2 inputs are required. Filter sets the NaN values to 1."""

    def _multiply(x, y):
        x = np.nan_to_num(x, nan=1)
        y = np.nan_to_num(y, nan=1)
        x = np.ma.masked_array(x, mask=np.isnan(x) & np.isnan(y))
        y = np.ma.masked_array(y, mask=x.mask)
        return (x * y).filled(np.nan)

    func = _multiply if filter else np.multiply

    with np.errstate(over='ignore'):
        return reduce(func, args)


def nan_mask(x, y):
    """replace input with NAN if input's corresponding mask value or the second input here, is negative."""
    x = x.copy()
    x[y < 0] = np.nan
    return x


def nan_out(x, lower=0, upper=0):
    """If x < lower or x > upper return NaN, else return x. At least one of "lower", "upper" is required."""
    return np.clip(x, a_min=lower, a_max=upper)


def power(x, y):
    """x ^ y"""
    with np.errstate(divide='ignore', invalid='ignore'):
        r = np.power(x, y)
        # 有可能产生inf，是否需要处理
        # r[np.isinf(r)] = np.nan
        return r


def purify(x):
    """Clear infinities (+inf, -inf) by replacing with NaN."""
    x = x.copy()
    x[np.isinf(x)] = np.nan
    return x


def replace(x, target=[-np.inf, np.inf], dest=[np.nan, np.nan]):
    """Replace target values in input with destination values."""
    x = x.copy()
    for t, d in zip(target, dest):
        x[x == t] = d
    return x


def reverse(x):
    """- x"""
    return -x


def round(x):
    """Round input to closest integer."""
    return np.around(x)


def round_down(x, f=1):
    """Round input to greatest multiple of f less than input;"""
    with np.errstate(invalid='ignore', divide='ignore'):
        return x // f * f


def sign(x):
    """if input = NaN; return NaN
else if input > 0, return 1
else if input < 0, return -1
else if input = 0, return 0

    return (0 < x) * 1 - (x < 0)
    """
    return np.sign(x)


def signed_power(x, y):
    """x raised to the power of y such that final result preserves sign of x."""
    with np.errstate(invalid='ignore', divide='ignore'):
        return sign(x) * (abs(y) ** y)


def s_log_1p(x):
    """Confine function to a shorter range using logarithm such that higher input remains higher and negative input remains negative as an output of resulting function and -1 or 1 is an asymptotic value."""
    with np.errstate(invalid='ignore', divide='ignore'):
        return sign(x) * log(1 + abs(x))


def sqrt(x):
    """Square root of x"""
    with np.errstate(invalid='ignore'):
        return np.sqrt(x)


def subtract(*args, filter=False):
    """x-y. If filter = true, filter all input NaN to 0 before subtracting"""

    def _subtract(x, y):
        x = np.nan_to_num(x, nan=0)
        y = np.nan_to_num(y, nan=0)
        x = np.ma.masked_array(x, mask=np.isnan(x) & np.isnan(y))
        y = np.ma.masked_array(y, mask=x.mask)
        return (x - y).filled(np.nan)

    func = _subtract if filter else np.subtract

    with np.errstate(over='ignore'):
        return reduce(func, args)


def to_nan(x, value=0, reverse=False):
    """Convert value to NaN or NaN to value if reverse=true"""
    x = x.copy()
    if reverse:
        x[np.isnan(x)] = value
    else:
        x[x == value] = np.nan
    return x


def densify(x):
    """Converts a grouping field of many buckets into lesser number of only available buckets so as to make working with grouping fields computationally efficient."""
    return x
