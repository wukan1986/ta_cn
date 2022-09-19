import numpy as np

from .wq.cross_sectional import rank as RANK


def cut(x, bins=[0, 10, 100, 1000, 10000], rank=True, pct=False):
    """返回的值最小值一般是1，但如果原值小于bins，那么最小值是0"""
    if rank:
        x = RANK(x, pct=pct)
    return np.digitize(x, bins, right=True)


def qcut(x, q=[0, 0.5, 1], rank=True, pct=True):
    if rank:
        x = RANK(x, pct=pct)
    return np.digitize(x, bins=q, right=True)


def top_k(x, bins=[0, 50, 100, 200]):
    """前N权重字典。正序，越小排名越靠前。所以用户可能需要主动取负数

    Parameters
    ----------
    x
    bins

    """
    labels = cut(x, bins=bins, rank=True, pct=False)
    # 前200=前50+前50到100+前100到200
    d = {k: np.where(labels <= i, x, np.nan) for i, k in enumerate(bins) if k > 0}

    return d


def quantile_n(x, n=10):
    """分位数权重

    Parameters
    ----------

    Returns
    -------

    """
    q = np.linspace(0, 1, n + 1)

    # 根据因子大小值进行百分位分层，数少就少分几层
    labels = qcut(x, q=q, rank=True, pct=True)

    # 因子分层，在这里就已经过滤只看几组，减少内存
    d = {k: np.where(labels == i, x, np.nan) for i, k in enumerate(q) if k > 0}

    return d
