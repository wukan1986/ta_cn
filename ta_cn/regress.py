import warnings

import bottleneck as _bn
import numba
import numpy as _np

from ta_cn import talib as _ta2d
from .nb import numpy_rolling_apply, _rolling_func_1_nb, _rolling_func_2_nb
from .utils import pd_to_np


@numba.jit(nopython=True, cache=True, nogil=True)
def _slope_nb(y, x, m_x):
    """slope线性回归斜率"""
    m_y = _np.mean(y)
    return _np.sum((x - m_x) * (y - m_y)) / _np.sum((x - m_x) ** 2)


@numba.jit(nopython=True, cache=True, nogil=True)
def _slope_yx_nb(y, x):
    """slope线性回归斜率"""
    m_x = _np.mean(x)
    m_y = _np.mean(y)
    return _np.sum((x - m_x) * (y - m_y)) / _np.sum((x - m_x) ** 2)


def FORCAST(real, timeperiod=14):
    """线性回归预测值

    Parameters
    ----------
    real
    timeperiod

    References
    ----------
    https://github.com/TA-Lib/ta-lib/blob/master/src/ta_func/ta_LINEARREG.c

    """
    return _ta2d.LINEARREG(real, timeperiod=timeperiod)


def SLOPE(real, timeperiod=14):
    """线性回归斜率

    Parameters
    ----------
    real
    timeperiod

    References
    ----------
    https://github.com/TA-Lib/ta-lib/blob/master/src/ta_func/ta_LINEARREG_SLOPE.c

    """
    return _ta2d.LINEARREG_SLOPE(real, timeperiod=timeperiod)


def SLOPE_NB(real, timeperiod=14):
    """numba版，输出结果也一样"""
    x = _np.arange(timeperiod)
    m_x = _np.mean(x)
    return numpy_rolling_apply([pd_to_np(real)], timeperiod, _rolling_func_1_nb, _slope_nb, x, m_x)


def SLOPE_YX_NB(real0, real1, timeperiod=30):
    """与talib.BETA不一样，talib将price转return后再回归"""
    return numpy_rolling_apply([pd_to_np(real0), pd_to_np(real1)],
                               timeperiod, _rolling_func_2_nb, _slope_yx_nb)


def ts_simple_regress(y, x, window=10):
    """滚动一元线性回归。比SLOPE_YX_NB快一些

    Parameters
    ----------
    y: array_like
        回归因变量
    x: array_like
        回归自变量
    window
        移动计算窗口长度

    Returns
    -------
    intercept_hat: ndarray
        回归截距项
    beta_hat: ndarray
        回归系数项
    residual_hat: ndarray
        回归残差项

    """
    xy_ts_sum = _bn.move_sum(_np.multiply(x, y), window=window, axis=0)
    xx_ts_sum = _bn.move_sum(_np.multiply(x, x), window=window, axis=0)
    x_bar = _bn.move_mean(x, window=window, axis=0)
    y_bar = _bn.move_mean(y, window=window, axis=0)

    up = xy_ts_sum - _np.multiply(x_bar, y_bar) * window
    down = xx_ts_sum - _np.multiply(x_bar, x_bar) * window
    beta_hat = up / down
    intercept_hat = y_bar - _np.multiply(beta_hat, x_bar)
    residual_hat = y - intercept_hat - _np.multiply(beta_hat, x)

    return intercept_hat, beta_hat, residual_hat


@numba.jit(nopython=True, cache=True, nogil=True)
def _ols_nb(y, x):
    # m = np.dot((np.dot(np.linalg.inv(np.dot(x.T, x)), x.T)), y)
    # residual = y - x.dot(m)
    return _np.dot((_np.dot(_np.linalg.inv(_np.dot(x, x.T)), x)), y)


def yx_rolling_apply(y, x, window, func1, func2, *args):
    """滚动应用方法 处理两个"""
    out = _np.empty_like(x)
    try:
        # 可能出现类似int无法设置nan的情况
        out[:window] = _np.nan
    except:
        out[:window] = 0

    arrs = [_np.lib.stride_tricks.sliding_window_view(i, window, axis=0) for i in (y, x)]

    return func1(*arrs, out, window, func2, *args)


warnings.filterwarnings("ignore", category=numba.NumbaPerformanceWarning)


# NumbaPerformanceWarning: np.dot() is faster on contiguous arrays, called on (array(float64, 2d, C), readonly array(float64, 1d, A))
#   out[i + timeperiod - 1] = func(yy, xx, *args)
@numba.jit(nopython=True, cache=True, nogil=True)
def _rolling_func_yx_nb(y, x, out, timeperiod, func, *args):
    if x.ndim == 3:
        for i, (yy, xx) in enumerate(zip(y, x)):
            out[i + timeperiod - 1] = func(yy, xx, *args)

    return out


def ts_multiple_regress(y, x, timeperiod=10, add_constant=True):
    """多元线性回归"""
    _y = pd_to_np(y)
    _x = pd_to_np(x)
    if add_constant:
        tmp = _np.ones(shape=(_x.shape[0], _x.shape[1] + 1))
        tmp[:, 1:] = _x
        _x = tmp
    coef = yx_rolling_apply(_y, _x, timeperiod, _rolling_func_yx_nb, _ols_nb)
    return coef, _y - _np.sum(_x * coef, axis=1)
