import numpy as np

from . import bn_wraps as bn
from .utils import pd_to_np
from .wq.cross_sectional import winsorize, zscore, scale


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
        _median = bn.nanmedian(x_, axis=1)[:, None]
        _mad = bn.nanmedian(abs(x - _median), axis=1)[:, None]
    else:
        _median = bn.nanmedian(x_)
        _mad = bn.nanmedian(abs(x - _median))

    _mad = _mad * constant * n

    return np.clip(x_, _median - _mad, _median + _mad)


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
        q = np.nanquantile(x_, [min_, max_], axis=1)
        return np.clip(x_, q[0][:, None], q[1][:, None])
    else:
        q = np.nanquantile(x_, [min_, max_])
        return np.clip(x_, q[0], q[1])


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
        q = np.nanquantile(x_, [min_, max_], axis=1)
        x_ = np.where(x_ < q[0][:, None], np.nan, x_)
        x_ = np.where(x_ > q[1][:, None], np.nan, x_)
    else:
        q = np.nanquantile(x_, [min_, max_])
        x_ = np.where(x_ < q[0], np.nan, x_)
        x_ = np.where(x_ > q[1], np.nan, x_)

    return x_


"""
标准化
"""


def fill_na(x):
    """用中位数填充，还是用平均值填充？

    -1到1归一化的值，用0填充也行吧？
    """
    x = x.copy()
    x[np.isnan(x)] = np.nanmedian(x)
    return x


def demean(x):
    """行业中性化，需要与groupby配合使用

    RuntimeWarning: Mean of empty slice
    nanmean在全nan时报此警告。这个警告还不好屏蔽
    """
    return x - np.nanmean(x)


# worldquant中函数的别名
winsorize_3sigma = winsorize
standardize_zscore = zscore
standardize_minmax = scale
