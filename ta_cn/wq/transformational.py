"""
Transformational Operators
"""
import numpy as np


def arc_cos(x):
    """If -1 <= x <= 1: arccos(x); else NaN"""
    return np.arccos(x)


def arc_sin(x):
    """If -1 <= x <= 1: arcsin(x); else NaN"""
    return np.arcsin(x)


def arc_tan(x):
    """This operator does inverse tangent of input. """
    return np.arctan(x)


def bucket(x, range="0, 1, 0.1", buckets="2,5,6,7,10"):
    """Convert float values into indexes for user-specified buckets. Bucket is useful for creating group values, which can be passed to group operators as input."""
    pass


def clamp(x, lower=0, upper=0, inverse=False, mask=""):
    """Limits input value between lower and upper bound in inverse = false mode (which is default). Alternatively, when inverse = true, values between bounds are replaced with mask, while values outside bounds are left as is."""
    pass


def filter(x, h="1, 2, 3, 4", t="0.5"):
    """Used to filter the value and allows to create filters like linear or exponential decay."""
    pass


def keep(x, f, period=5):
    """This operator outputs value x when f changes and continues to do that for “period” days after f stopped changing. After “period” days since last change of f, NaN is output."""
    pass


def left_tail(x, maximum=0):
    """NaN everything greater than maximum, maximum should be constant."""
    pass


def pasteurize(x):
    """Set to NaN if x is INF or if the underlying instrument is not in the Alpha universe"""
    pass


def right_tail(x, minimum=0):
    """NaN everything less than minimum, minimum should be constant."""
    pass


def sigmoid(x):
    """Returns 1 / (1 + exp(-x))"""
    pass


def tail(x, lower=0, upper=0, newval=0):
    """If (x > lower AND x < upper) return newval, else return x. Lower, upper, newval should be constants. """
    pass


def tanh(x):
    """Hyperbolic tangent of x"""
    pass


def trade_when(x, y, z):
    """Used in order to change Alpha values only under a specified condition and to hold Alpha values in other cases. It also allows to close Alpha positions (assign NaN values) under a specified condition."""
    pass
