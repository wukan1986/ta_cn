import numpy as _np

from . import bn_wraps as _bn
from .utils import pd_to_np


def winsorize_mad(x, n=3, constant=1.4826):
    """缩尾去极值，MAD法

    Parameters
    ----------
    x: array
        需要缩尾去极值的数据
    n: float
        设置范围大小
    constant: float
        比例因子。为了能将MAD当作标准差估计的一种一致估计量，使用两者之间的关联。其中比例因子常量k的值取决于分布类型，在正态分布下该常量约等于1.4826

        .. math:: \hat {\sigma } = k * MAD

    Returns
    -------
    array
        `x` 经过MAD法缩尾去极值处理后的新数据

    References
    ----------
    https://en.wikipedia.org/wiki/Median_absolute_deviation


    """
    x_ = pd_to_np(x, copy=False)
    if x_.ndim == 2:
        _median = _bn.nanmedian(x_, axis=1)[:, None]
        _mad = _bn.nanmedian(abs(x - _median), axis=1)[:, None]
    else:
        _median = _bn.nanmedian(x_)
        _mad = _bn.nanmedian(abs(x - _median))

    _mad = _mad * constant * n

    return _np.clip(x_, _median - _mad, _median + _mad)


def winsorize_3sigma(x, min_=-3, max_=3, ddof=0):
    """缩尾去极值，三倍标准差法

    Parameters
    ----------
    x: array
        需要缩尾去极值的数据
    min_: float
        设置下界标准差倍数
    max_: float
        设置上界标准差倍数
    ddof: int
        计算标准差的过程中分母为N - ddof：求标准差时默认除以 n 的，即是有偏的，ddof = 0；计算无偏样本标准差方式为除以 n-1 ，加入参数 ddof = 1

    Returns
    -------
    array
        `x` 经过三倍标准差法缩尾去极值处理后的新数据

    """

    x_ = pd_to_np(x, copy=False)
    if x_.ndim == 2:
        _mean = _bn.nanmean(x_, axis=1)[:, None]
        _std = _bn.nanstd(x_, axis=1, ddof=ddof)[:, None]
    else:
        _mean = _bn.nanmean(x_)
        _std = _bn.nanstd(x_, ddof=ddof)

    return _np.clip(x_, _mean + _std * min_, _mean + _std * max_)


def winsorize_quantile(x, min_=0.1, max_=0.9):
    """缩尾去极值，分位数法

    Parameters
    ----------
    x: array
        需要缩尾去极值的数据
    min_: float
        设置下界分位数
    max_: float
        设置上界分位数

    Returns
    -------
    array
        `x` 经过分位数法缩尾去极值处理后的新数据

    """

    x_ = pd_to_np(x, copy=False)
    if x_.ndim == 2:
        q = _np.nanquantile(x_, [min_, max_], axis=1)
        return _np.clip(x_, q[0][:, None], q[1][:, None])
    else:
        q = _np.nanquantile(x_, [min_, max_])
        return _np.clip(x_, q[0], q[1])


"""
删除极值
"""


def drop_quantile(x, min_=0.1, max_=0.9):
    """删除去极值，分位数法

    Parameters
    ----------
    x: array
        需要删除去极值的数据
    min_: float
        设置下界分位数
    max_: float
        设置上界分位数

    Returns
    -------
    array
        `x` 经过分位数法删除去极值处理后的新数据

    """

    x_ = pd_to_np(x, copy=False)
    if x_.ndim == 2:
        q = _np.nanquantile(x_, [min_, max_], axis=1)
        x_ = _np.where(x_ < q[0][:, None], _np.nan, x_)
        x_ = _np.where(x_ > q[1][:, None], _np.nan, x_)
    else:
        q = _np.nanquantile(x_, [min_, max_])
        x_ = _np.where(x_ < q[0], _np.nan, x_)
        x_ = _np.where(x_ > q[1], _np.nan, x_)

    return x_


"""
标准化
"""


def standardize_zscore(x, ddof=0):
    """zscore标准化

    Parameters
    ----------
    x: 2d array
        需要进行zscore标准化的数据
    ddof: int
        计算标准差的过程中分母为N - ddof：求标准差时默认ddof = 0；计算无偏样本标准差时ddof = 1

    Returns
    -------
    2d array
        `x` 经过zscore标准化后的新数据

    """

    x_ = pd_to_np(x, copy=False)
    if x_.ndim == 2:
        _mean = _bn.nanmean(x_, axis=1)[:, None]
        _std = _bn.nanstd(x_, axis=1, ddof=ddof)[:, None]
    else:
        _mean = _bn.nanmean(x_)
        _std = _bn.nanstd(x_, ddof=ddof)

    return (x_ - _mean) / _std


def standardize_minmax(x, min_=0, max_=1):
    """MinMax归一化

    Parameters
    ----------
    x: array
        需要进行MinMax归一化的数据
    min_: float
        归一化范围的下界
    max_: float
        归一化范围的上界

    Returns
    -------
    array
        `x` 经过MinMax归一化后的新数据


    """
    x_ = pd_to_np(x, copy=False)
    if x_.ndim == 2:
        _min = _bn.nanmin(x_, axis=1)[:, None]
        _max = _bn.nanmax(x_, axis=1)[:, None]
    else:
        _min = _bn.nanmin(x_)
        _max = _bn.nanmax(x_)

    _std = (x_ - _min) / (_max - _min)
    return (max_ - min_) * _std + min_


def fill_na(x):
    """用中位数填充，还是用平均值填充？

    -1到1归一化的值，用0填充也行吧？
    """
    x = x.copy()
    x[_np.isnan(x)] = _np.nanmedian(x)
    return x


def demean(x):
    """行业中性化，需要与groupby配合使用

    RuntimeWarning: Mean of empty slice
    nanmean在全nan时报此警告。这个警告还不好屏蔽
    """
    return x - _np.nanmean(x)
