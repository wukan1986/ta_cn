import warnings

import numba
import numpy as np
import pandas as pd

from . import bn_wraps as bn
from . import talib as ta
from .nb import numpy_rolling_apply, _rolling_func_1_nb, _rolling_func_2_nb
from .utils import pd_to_np

_ta1d = ta.init(mode=1, skipna=False)
_ta2d = ta.init(mode=2, skipna=False)

# 通达信，线性回归预测值
FORCAST = _ta2d.LINEARREG
# 通达信，线性回归斜率
SLOPE = _ta2d.LINEARREG_SLOPE


def SLOPE_Y(real, timeperiod):
    """numba版，输出结果与LINEARREG_SLOPE一样

    SLOPE_Y(real, timeperiod=14)
    """

    @numba.jit(nopython=True, cache=True, nogil=True)
    def _slope_y_nb(y, x, m_x):
        """slope线性回归斜率。由于x固定，所以提前在外部计算，加快速度"""
        m_y = np.mean(y)
        return np.sum((x - m_x) * (y - m_y)) / np.sum((x - m_x) ** 2)

    x = np.arange(timeperiod)
    m_x = np.mean(x)
    return numpy_rolling_apply([pd_to_np(real)], timeperiod, _rolling_func_1_nb, _slope_y_nb, x, m_x)


def SLOPE_YX(real0, real1, timeperiod):
    """与talib.BETA不一样，talib将price转return后再回归

    SLOPE_YX(real0, real1, timeperiod=30)
    """

    @numba.jit(nopython=True, cache=True, nogil=True)
    def _slope_yx_nb(y, x):
        """slope线性回归斜率。y与x是一直变化的"""
        m_x = np.mean(x)
        m_y = np.mean(y)
        return np.sum((x - m_x) * (y - m_y)) / np.sum((x - m_x) ** 2)

    return numpy_rolling_apply([pd_to_np(real0), pd_to_np(real1)],
                               timeperiod, _rolling_func_2_nb, _slope_yx_nb)


def ts_simple_regress(y, x, window=10):
    """滚动一元线性回归。

    由于利用了bottleneck的滚动功能，比SLOPE_YX_NB快一些，但精度有少量差异，后期需再验证

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
    xy_ts_sum = bn.move_sum(np.multiply(x, y), window=window, axis=0)
    xx_ts_sum = bn.move_sum(np.multiply(x, x), window=window, axis=0)
    x_bar = bn.move_mean(x, window=window, axis=0)
    y_bar = bn.move_mean(y, window=window, axis=0)

    up = xy_ts_sum - np.multiply(x_bar, y_bar) * window
    down = xx_ts_sum - np.multiply(x_bar, x_bar) * window
    beta_hat = up / down
    intercept_hat = y_bar - np.multiply(beta_hat, x_bar)
    residual_hat = y - intercept_hat - np.multiply(beta_hat, x)

    return intercept_hat, beta_hat, residual_hat


warnings.filterwarnings("ignore", category=numba.NumbaPerformanceWarning)


def ts_multiple_regress(y, x, timeperiod=10, add_constant=True):
    """时序上滚动多元线性回归

    Parameters
    ----------
    y: 1d array
        因变量。一维
    x: 2d array
        自变量。二维。一列为一个特征
    timeperiod:int
        周期
    add_constant: bool
        是否添加常量

    Returns
    -------
    coef:
        系数。与x形状类似，每个特性占一例。时序变化，所以每天都有一行
    residual:
        残差。与y形状类似，由实际y-预测y而得到

    """

    @numba.jit(nopython=True, cache=True, nogil=True)
    def _rolling_func_xy_nb(x, y, out, timeperiod, func, *args):
        """滚动多元"""
        if x.ndim == 3:
            for i, (yy, xx) in enumerate(zip(y, x)):
                out[i + timeperiod - 1] = func(yy, xx, *args)

        return out

    @numba.jit(nopython=True, cache=True, nogil=True)
    def _ts_ols_nb(y, x):
        """使用可逆矩阵计算多元回归。

        由于sliding_window_view后的形状再enumerate后比较特殊，所以原公式的转置进行了调整
        """
        return np.dot((np.dot(np.linalg.inv(np.dot(x, x.T)), x)), y)

    _y = pd_to_np(y)
    _x = pd_to_np(x)
    if add_constant:
        tmp = np.ones(shape=(_x.shape[0], _x.shape[1] + 1))
        tmp[:, 1:] = _x
        _x = tmp

    coef = numpy_rolling_apply([_x, _y], timeperiod, _rolling_func_xy_nb, _ts_ols_nb)
    y_hat = np.sum(_x * coef, axis=1)
    residual = _y - y_hat
    return coef, residual


def multiple_regress(y, x, add_constant=True):
    """横截面上的多元回归。主要用于中性化多元回归场景

    需要先按日期进行groupby，然后再应用回归函数
    """

    @numba.jit(nopython=True, cache=True, nogil=True)
    def _cs_ols_nb(y, x):
        """使用可逆矩阵计算多元回归。

        标准的多元回归
        """
        return np.dot((np.dot(np.linalg.inv(np.dot(x.T, x)), x.T)), y)

    _y = pd_to_np(y)
    _x = pd_to_np(x)
    if add_constant:
        if _x.ndim == 1:
            # 一维数据转成二维数据
            _x = _x.reshape(-1, 1)
        tmp = np.ones(shape=(_x.shape[0], _x.shape[1] + 1))
        tmp[:, 1:] = _x
        _x = tmp
    coef = _cs_ols_nb(_y, _x)
    y_hat = np.sum(_x * coef, axis=1)
    residual = _y - y_hat
    return residual, y_hat, coef


def REGRESI(y, *args, timeperiod=60):
    if isinstance(y, pd.Series):
        x = pd.concat(args, axis=1)
    else:
        x = np.concatenate(args, axis=1)
    coef, resi = ts_multiple_regress(y, x, timeperiod=timeperiod, add_constant=True)
    return resi
