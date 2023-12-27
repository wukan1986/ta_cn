import numba
import numpy as np

from .. import bn_wraps as bn
from ..nb import numpy_rolling_apply_1, _rolling_func_1_1_nb
from ..utils import pd_to_np


@numba.jit(nopython=True, cache=True, nogil=True)
def _avedev_nb(a):
    """avedev平均绝对偏差"""
    return np.mean(np.abs(a - np.mean(a)))


def AVEDEV(real, timeperiod: int):
    """平均绝对偏差

    AVEDEV(real, timeperiod=20)
    """
    return numpy_rolling_apply_1([pd_to_np(real)], timeperiod, _rolling_func_1_1_nb, _avedev_nb)


def STD(x, d):
    """样本标准差"""
    return bn.move_std(x, window=d, axis=0, ddof=1)


def STDP(x, d):
    """总体标准差"""
    return bn.move_std(x, window=d, axis=0, ddof=0)


def VAR(x, d):
    """样本方差"""
    return bn.move_var(x, window=d, axis=0, ddof=1)


def VARP(x, d):
    """总体方差"""
    return bn.move_var(x, window=d, axis=0, ddof=0)


@numba.jit(nopython=True, cache=True, nogil=True)
def _limit_count_nb(arr, out1, out2, d):
    is_1d = arr.ndim == 1
    x = arr.shape[0]
    y = 1 if is_1d else arr.shape[1]

    for j in range(y):
        a = arr if is_1d else arr[:, j]
        nn = out1 if is_1d else out1[:, j]
        mm = out2 if is_1d else out2[:, j]
        n = 0  # N天
        m = 0  # M板
        k = 0  # 连续False个数
        f = True  # 前面的False不处理
        for i in range(x):
            if a[i]:
                # 正常统计
                k = 0
                n += 1
                m += 1
                nn[i] = n
                mm[i] = m
                f = False
            else:
                if f:
                    continue
                k += 1  # 非False计数
                nn[i] = -k  # 表示离上涨停的天数，-1表示昨天是涨停的
                if k > d:
                    m = 0
                    n = 0
                else:
                    n += 1
                mm[i] = 0
    # N天M板
    return out1, out2


def limit_count(x, d):
    """涨停统计

    BARSLASTCOUNT可以统计连板数。但无法统计N天M板这种情况.

    Parameters
    ----------
    x
    d: int
        0表示必须连板
        1表示可以间隔1天板。出现5天3板，9天5板都是有可能的
        2表示可以间隔2天板。所以4天2板这种情况一定要用2才能区分
        3以此类推

    Returns
    -------
    out1
        总天数。小于0时，表示前几天是涨停。大于0时是累计天数
    out2
        板数。累计连板数。断板时会延用上次板数d天时间

    Examples
    --------
    >>> a = np.array([0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1])
    >>> b, c = limit_count(a, 2)
    >>> print(a)
    >>> print(b)
    >>> print(c)

    >>> [0 1 0 1 1 0 0 1 1 0 0 0 0 1]
    >>> [0 1 -1  3  4 -1 -2  1  2 -1 -2 -3 -4  1]
    >>> [0 1  0  2  3  0  0  1  2  0  0  0  0  1]

    解读一下，如：
    0. 无
    1. 1天1板
    2. 昨天1天1板
    3. 3天2板
    4. 4天3板
    5. 昨天4天3板
    6. 前天4天3板
    7. 1天1板
    8. 2天2板

    """
    x = pd_to_np(x, copy=False)
    out1 = np.zeros_like(x, dtype=int)
    out2 = np.zeros_like(x, dtype=int)
    return _limit_count_nb(x, out1, out2, d)
