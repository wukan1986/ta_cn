"""
ATR与STD也是一种度量波动的方法，这里不再提供

以下方法来自于Trading Systems and Methods, Chapter 1, Measuring Noise

References
----------
https://zhuanlan.zhihu.com/p/544744582

"""
from .wq.arithmetic import abs_, sqrt, log
from .wq.time_series import ts_delta, ts_sum, ts_max, ts_min


def efficiency_ratio(x, d):
    """效率系数。值越大，噪音越小。最大值为1，最小值为0

    本质上是位移除以路程
    """
    t1 = abs_(ts_delta(x, d))
    t2 = ts_sum(abs_(ts_delta(x, 1)), d)
    return t1 / t2


def price_density(high, low, d):
    """价格密度。值越大，噪音越大

    如果K线高低相连，上涨为1，下跌也为1
    如果K线高低平行，值大于1，最大为d
    """
    t1 = ts_sum(high - low, d)
    t2 = ts_max(high) - ts_min(low)
    return t1 / t2


def fractal_dimension(high, low, close, d):
    """分形维度。值越大，噪音越大"""
    t1 = ts_max(high) - ts_min(low)
    t2 = ts_delta(close, 1)  # TODO: 这里是否要求绝对值?
    t3 = (1 / d) ** 2
    L = ts_sum(sqrt(t3 + t2 / t1), d)
    return 1 + (log(L) + log(2)) / log(2 * d)
