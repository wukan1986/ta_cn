"""
Transformational Operators
"""
import numba
import numpy as np

from .. import numba_cache
from ..utils import pd_to_np
from ..wq.logical import if_else
from ..wq.time_series import days_from_last_change


def arc_cos(x):
    """If -1 <= x <= 1: arccos(x); else NaN"""
    return np.arccos(x)


def arc_sin(x):
    """If -1 <= x <= 1: arcsin(x); else NaN"""
    return np.arcsin(x)


def arc_tan(x):
    """This operator does inverse tangent of input. """
    return np.arctan(x)


def bucket(x,
           range="0, 1, 0.1",
           buckets="2,5,6,7,10",
           skipBegin=False, skipEnd=False, skipBoth=False,
           NANGroup=True):
    """Convert float values into indexes for user-specified buckets. Bucket is useful for creating group values, which can be passed to group operators as input."""
    pass


def clamp(x, lower=0, upper=0, inverse=False, mask=np.nan):
    """Limits input value between lower and upper bound in inverse = false mode (which is default). Alternatively, when inverse = true, values between bounds are replaced with mask, while values outside bounds are left as is."""
    if inverse:
        # mask is one of: 'nearest_bound', 'mean', 'NAN' or any floating point number
        return if_else((x > lower) & (x < upper), mask, x)
    else:
        # q = if_else(x < lower, lower, x)
        # u = if_else(q > upper, upper, q)
        return np.clip(x, lower, upper)


def filter(x, h="1, 2, 3, 4", t="0.5"):
    """Used to filter the value and allows to create filters like linear or exponential decay."""
    pass


def keep(x, f, period=5):
    """This operator outputs value x when f changes and continues to do that for “period” days after f stopped changing. After “period” days since last change of f, NaN is output."""
    D = days_from_last_change(f)
    return trade_when(D < period, x, D > period)


def left_tail(x, maximum=0):
    """NaN everything greater than maximum, maximum should be constant."""
    return np.where(x > maximum, np.nan, x)


def pasteurize(x):
    """Set to NaN if x is INF or if the underlying instrument is not in the Alpha universe"""
    # TODO: 不在票池中的的功能无法表示
    x = x.copy()
    x[np.isinf(x)] = np.nan
    return x


def right_tail(x, minimum=0):
    """NaN everything less than minimum, minimum should be constant."""
    return np.where(x < minimum, np.nan, x)


def sigmoid(x):
    """Returns 1 / (1 + exp(-x))"""
    return 1 / (1 + np.exp(-x))


def tail(x, lower=0, upper=0, newval=0):
    """If (x > lower AND x < upper) return newval, else return x. Lower, upper, newval should be constants. """
    return np.where((x > lower) & (x < upper), newval, x)


def tanh(x):
    """Hyperbolic tangent of x"""
    return np.tanh(x)


def trade_when(x, y, z):
    """Used in order to change Alpha values only under a specified condition and to hold Alpha values in other cases. It also allows to close Alpha positions (assign NaN values) under a specified condition."""

    @numba.jit(nopython=True, cache=numba_cache, nogil=True)
    def _trade_when_nb(xx, yy, zz, out):
        is_1d = xx.ndim == 1
        x = xx.shape[0]
        y = 1 if is_1d else xx.shape[1]

        for j in range(y):
            a = xx if is_1d else xx[:, j]
            b = yy if is_1d else yy[:, j]
            c = zz if is_1d else zz[:, j]
            d = out if is_1d else out[:, j]
            last = np.nan
            for i in range(x):
                if c[i] > 0:
                    d[i] = np.nan
                elif a[i] > 0:
                    d[i] = b[i]
                else:
                    d[i] = last
                last = d[i]

        return out

    x = pd_to_np(x, copy=False)
    y = pd_to_np(y, copy=False)
    z = pd_to_np(z, copy=False)
    out = np.empty_like(y)
    return _trade_when_nb(x, y, z, out)
