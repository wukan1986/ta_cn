import numpy as _np

from ta_cn.utils import np_to_pd


def _MA_EMA(real, timeperiod, com=None, span=None, alpha=None):
    """内部函数，已经废弃。先计算MA做第一个值，然后再算EMA
    二维矩阵如果开头有NaN，那么求均值的位置就不统一，得做特别处理
    好不容易想出来的，删了可惜
    """
    real = np_to_pd(real, copy=True)  # 开头部分将写入SMA
    ma = np_to_pd(_np.zeros_like(real), copy=False)  # 来计算sma

    # 取最长位置, 用于计算SMA，没有必要全算一次MA
    max_end = real.notna().idxmax() + timeperiod
    if hasattr(max_end, 'max'):
        max_end = max_end.max()

    # 计算ma
    ma[:max_end] = real[:max_end].rolling(window=timeperiod, min_periods=timeperiod).mean()
    # 计算需要复制的区域,此区前部分为NaN,最后为mean
    mask = ma.isna().shift(fill_value=True)
    real[mask] = ma
    return real.ewm(com=com, span=span, alpha=alpha, min_periods=0, adjust=False).mean()