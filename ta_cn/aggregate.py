import numpy as _np


def A_div_AB(x):
    """A/(A+B)

    输入一维，得到一个值
    输入二维，得到一列值

    可用于计算市场宽度等指标
    """
    if x.ndim == 2:
        t1 = _np.nansum(x, axis=1, keepdims=True)
        t2 = _np.nansum(~_np.isnan(x), axis=1, keepdims=True)
    else:
        t1 = _np.nansum(x)
        t2 = _np.nansum(~_np.isnan(x))
    return t1 / t2
