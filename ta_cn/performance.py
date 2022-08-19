"""
# 计算说明
计算是需要在 `快` 与 `精` 中进行平衡，大规模计算时使用`快速评估`，然后再使用工具进行高精度回测

## 核心
1. 对于单一投资品的收益率，对数收益率时序上可加
2. 对于不同投资品的收益率，应该用简单收益率，因为它在截面上有可加性

## fast，快速计算
1. 不考虑手续费、滑点等信息，否则代码过于复杂。一般用于大规模挖掘时使用，挖出的结果再进行中高精度计算
2. 使用对数收益率累加比简单收益率累乘，计算更快
3. 信号操作需要转换成持仓状态才能使用。信号一般要下移一格才是持仓
4. 做空时收益计算有误差，但在涨跌幅不大时，可以忽略
5. 收益计算，本质上是段内单利，段间复利。但以前使用的收益率累乘，相当于每天调仓为一段，变成了每天复利，
    所以如果代码是每月调仓，收益率就得换成每月，如果是不规则调仓，那就使用 (出场价/入场价-1) 进行计算
6. 持仓取值是1 0 -1还是0.5一类的呢？本质上是看操作的资金占总资金的比重
7. 如果持仓是-2 0 1 3等手数，那盈亏其实应当用diff差分，但这种情况下建议使用vectorbt

## medium, 中速计算
1. 使用快速的向量计算框架vectorbt
2. 可以灵活设置交易成本等信息

## slow, 慢速框架
1. 通常使用事件框架来实现。如backtrader、rqalpha、zipline、聚宽等
2. 与这些平台的交互都统一成因子值，此处不存因子表达式
3. 这些平台都当成算法交易执行工具进行回测

"""

from typing import Union

import numpy as np
import pandas as pd

from .utils import np_to_pd


def to_log_returns(prices: Union[pd.Series, pd.DataFrame]) -> Union[pd.Series, pd.DataFrame]:
    """对数收益率

    Parameters
    ----------
    prices:
        价格

    Returns
    -------
    对数收益率，时序上可加

    See Also
    --------
    ffn

    """
    prices = np_to_pd(prices).replace(0, np.nan)
    return np.log(prices / prices.shift(1))


def to_returns(prices: Union[pd.Series, pd.DataFrame], sub_one=True) -> Union[pd.Series, pd.DataFrame]:
    """简单收益率

    Parameters
    ----------
    prices
    sub_one

    Returns
    -------
    简单收益率，横截面上可加

    See Also
    --------
    ffn

    """
    prices = np_to_pd(prices).replace(0, np.nan)
    if sub_one:
        return prices / prices.shift(1) - 1.
    else:
        return prices / prices.shift(1)


def log_returns_cumsum(returns: Union[pd.Series, pd.DataFrame]) -> Union[pd.Series, pd.DataFrame]:
    """对数收益率累加

    Parameters
    ----------
    returns:
        简单收益率 / 对数收益率

    Notes
    -----
    - 简单收益率: cumsum得到的结果是单利。不建议用于做空
    - 对数收益率: cumsum得到的是log(pn/p1)，本质上是复利

    """
    returns = np_to_pd(returns)
    return returns.fillna(0.0).cumsum()


def returns_cumprod(returns: Union[pd.Series, pd.DataFrame], add_one=True) -> Union[pd.Series, pd.DataFrame]:
    """简单收益率累乘

    Parameters
    ----------
    returns
        简单收益率
    add_one

    Returns
    -------
    还原价格

    Notes
    -----
    - 简单收益率：cumprod得到的是复利
    - 对数收益率：不能累乘

    """
    returns = np_to_pd(returns)
    if add_one:
        # 简单收益率(减一过于的值)
        return returns.add(1., fill_value=0.0).cumprod()
    else:
        # 价格比(nan需要改成1) 1表示P1/P1
        return returns.fillna(1.).cumprod()


def log_returns_exp(returns: Union[pd.Series, pd.DataFrame]) -> Union[pd.Series, pd.DataFrame]:
    """对数收益率还原。还原后是Pn/P1比值，相当于净值

    to_returns(df)+1 = returns_exp(to_log_returns(df))

    -1 = log(exp(-1))
    1 = exp(log(1)) 。 log定义域>0

    Parameters
    ----------
    returns
        - 输入简单收益率：原数据没有经过log处理，还原无意义
        - 输入对数收益率：还原的只是价格比，-1后才是简单收益率
        - 累加对数收益率。还原后是以1为起点的净值

    """
    return np.exp(returns)


def equal_weighted_index(prices: Union[pd.Series, pd.DataFrame]) -> pd.Series:
    """等权重指数

    将多条价格或净值等权重合成一条指数

    1. 价格得到简单收益率。只有简单收益率才能横截面加和
    2. 得到横截面平均。自动跳过NaN
    3. 简单收益率只能累乘求复利
    4. 没有做空，一直是buy and hold，可以使用 简单收益率累乘复利

    Parameters
    ----------
    prices
        价格或净值

    Returns
    -------
    pd.Series
        指数或合成净值

    """
    # 不进行加1减1的操作，加快速度
    # 虽然是累乘，但由于只计算一列，所以速度还能接受
    return returns_cumprod(to_returns(prices, False).mean(axis=1), False)


def weighted_index(prices, weights):
    """加权指数

    Parameters
    ----------
    prices
        价格
    weights
        权重

    Returns
    -------
    加权指数

    """
    returns = to_returns(prices, False).fillna(1)
    weights = weights.div(weights.sum(axis=1), axis=0).fillna(0)
    return returns_cumprod((returns * weights).sum(axis=1), False)
