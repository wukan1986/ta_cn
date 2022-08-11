import numpy as _np

import ta_cn.bn_wraps as _bn
import ta_cn.talib as _ta2d
from .maths import MAX, ABS
from .nb import _filter_nb, _bars_last_nb, _bars_last_count_nb, numpy_rolling_apply, _bars_since_n_nb, \
    _rolling_func_1_nb, _product_nb
from .utils import pd_to_np


def CONST(real):
    """取A最后的值为常量"""
    return _np.full_like(real, real[-1])


def COUNT(real, timeperiod):
    """统计N周期中满足X条件的周期数"""
    return SUM(real, timeperiod)


def DIFF(real, timeperiod: int = 1):
    """差分"""
    return real - REF(real, timeperiod)


def HHV(real, timeperiod: int = 5):
    """求timeperiod周期内real最高值"""
    return _bn.move_max(real, window=timeperiod, axis=0)


def HHVBARS(real, timeperiod: int = 5):
    """求timeperiod周期内real最高值到当前周期数"""
    return _bn.move_argmax(real, window=timeperiod, axis=0)


def LLV(real, timeperiod: int = 5):
    """求timeperiod周期内real最低值"""
    return _bn.move_min(real, window=timeperiod, axis=0)


def LLVBARS(real, timeperiod: int = 5):
    """求timeperiod周期内real最低值到当前周期数"""
    return _bn.move_argmin(real, window=timeperiod, axis=0)


def REF(real, timeperiod: int = 1):
    """向前引用，特意模仿shift"""
    if timeperiod == 0 or _np.isnan(timeperiod):
        # 该不该复制呢？
        return real
    arr = _np.empty_like(real)
    if timeperiod > 0:
        arr[:timeperiod] = _np.nan
        arr[timeperiod:] = real[:-timeperiod]
    if timeperiod < 0:
        arr[timeperiod:] = _np.nan
        arr[:timeperiod] = real[-timeperiod:]
    return arr


def SUM(real, timeperiod: int = 5):
    """时序滚动求和

    Parameters
    ----------
    real
    timeperiod: int
        滚动周期
        0表示全量即累计求和

    """
    if timeperiod > 0:
        return _bn.move_sum(real, window=timeperiod, axis=0)
    else:
        # 0表示全量累计求和
        return _np.cumsum(real, axis=0)


def SUMIF(real, condition, timeperiod):
    """!!!注意，condition位置"""
    return _bn.move_sum(real * condition, window=timeperiod, axis=0)


def TR(high, low, close):
    """TR真实波幅"""
    lc = REF(close, 1)
    return MAX(high - low, ABS(high - lc), ABS(lc - low))


def MA(real, timeperiod: int = 5):
    """简单移动平均

    等价于talib中的SMA"""
    return _bn.move_mean(real, window=timeperiod, axis=0)


def FILTER(S, N):
    """FILTER函数，S满足条件后，将其后N周期内的数据置为0"""
    S = pd_to_np(S, copy=True)
    return _filter_nb(S, N)


def BARSLAST(S):
    """BARSLAST(X)，上一次X不为0到现在的天数

    成立当天输出0
    """
    S = pd_to_np(S, copy=False)
    out = _np.zeros_like(S, dtype=int)
    return _bars_last_nb(S, out)


def BARSLASTCOUNT(S):
    """BARSLASTCOUNT(X)，统计连续满足X条件的周期数

    成立第一天输出1
    """
    S = pd_to_np(S, copy=False)
    out = _np.zeros_like(S, dtype=int)
    return _bars_last_count_nb(S, out)


def BARSSINCEN(cond, timeperiod):
    """BARSSINCEN(X,N):N周期内第一次X不为0到现在的天数"""
    return numpy_rolling_apply([pd_to_np(cond)], timeperiod, _rolling_func_1_nb, _bars_since_n_nb, timeperiod)


def PRODUCT(real, timeperiod: int = 5):
    return numpy_rolling_apply([pd_to_np(real)], timeperiod, _rolling_func_1_nb, _product_nb)


def WMA(real, timeperiod: int = 5):
    return _ta2d.WMA(real, timeperiod=timeperiod)
