import numpy as np

from .utils import pd_to_np


def chip(open_, high, low, close, turnover,
         start=None, stop=None, step=0.1):
    """筹码分布，可用于WINNER或COST指标

    不可能完全还原真实的筹码分布，只能接近。所以我做了一下特别处理

    1. 不同价格分配了不同的权重
        - [low,high] 一倍权重
        - [open, close] 两倍权重。可自行修改
        - 三角权重等需要用户自行修改
    2. 步长自定义。没有必要每个价格都统计，特别是复权后价格也无法正好是0.01间隔
        高价股建议步长设大些，低价股步长需设小些


    Parameters
    ----------
    open_
    high
    low
    close
        一维序列
    turnover:
        换手率，需要在外转成0~1范围内
    start
        网格开始价格
    stop
        网格结束价格
    step
        步长。

    Returns
    -------
    out
        筹码分布
    grid
        价格网格

    """
    # 将类型进行转换，要提速时可以将此在外部实现
    open_ = pd_to_np(open_)
    high = pd_to_np(high)
    low = pd_to_np(low)
    close = pd_to_np(close)
    turnover = pd_to_np(turnover)

    # 网格范围
    if start is None:
        start = (np.floor(np.min(low) / step) - 1) * step
    if stop is None:
        stop = (np.ceil(np.max(high) / step) + 1) * step
    columns = np.arange(start, stop, step)

    # 初始化价格网格
    grid = np.zeros(shape=(len(turnover), len(columns)), dtype=float)
    grid[:] = columns

    # 权重
    weight = np.zeros_like(grid, dtype=int)
    # 输出
    out = np.zeros_like(grid, dtype=float)

    # 从最低到最高，等权1
    high = high.reshape(-1, 1) + step / 2
    low = low.reshape(-1, 1) - step / 2
    weight[(grid >= low) & (grid <= high)] = 1

    # 从开盘到收盘的实体。出现的概率高，时间长给2倍权重，用户可以自己改
    high = np.maximum(open_, close).reshape(-1, 1) + step / 2
    low = np.minimum(open_, close).reshape(-1, 1) - step / 2
    weight[(grid >= low) & (grid <= high)] = 2

    # 权重归一
    weight = weight / np.nansum(weight, axis=1, keepdims=True)
    # 剩余换手率
    turnover2 = 1 - turnover

    # 第一天其实应当用上市发行价，过于麻烦，还是将第一天等权
    # 取巧方法，利用-1的特性，可减少if判断，
    out[-1] = weight[0]

    # 这里现在用的numpy, 还要快可考虑numba
    for i in range(len(turnover)):
        out[i] = out[i - 1] * turnover2[i] + weight[i] * turnover[i]

    # out.sum(axis=1)
    return out, grid


def WINNER(out, grid, close):
    """获利盘比例

    Parameters
    ----------
    out
        chip函数生成的筹码分布矩阵
    grid
        价格网格
    close
        收盘价。或指定价

    Examples
    --------
    >>> out, grid = chip(open_, high, low, close, turnover, step=0.1)
    >>> WINNER(out, grid, turnover)


    """
    if isinstance(close, np.ndarray):
        close = close.reshape(-1, 1)

    cheap = np.where(grid <= close, out, 0)
    return np.sum(cheap, axis=1)


def COST(out, grid, cost):
    """成本分布

    Parameters
    ----------
    out
        chip函数生成的筹码分布矩阵
    grid
        价格网格
    cost
        成本

    Examples
    --------
    >>> out, grid = chip(open_, high, low, close, turnover, step=0.1)
    >>> COST(out, grid, 0.5)

    """
    if isinstance(cost, np.ndarray):
        cost = cost.reshape(-1, 1)
    cum = np.cumsum(out, axis=1)
    prices = np.where(cum <= cost, grid, 0)
    return np.max(prices, axis=1)
