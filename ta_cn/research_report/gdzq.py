"""
光大证券，研报复现
"""
from ..regress import ts_simple_regress
from ..wq.time_series import ts_zscore


def rsrs_v1(high, low, d):
    """阻力支撑相对强度(Resistance Support Relative Strength)"""
    beta = ts_simple_regress(high, low, d, lag=0, rettype=2)
    return beta


def rsrs_v2(high, low, d, m):
    """阻力支撑相对强度，标准化"""
    beta = ts_simple_regress(high, low, d, lag=0, rettype=2)
    return ts_zscore(beta, m)


def rsrs_v3(high, low, d, m):
    """阻力支撑相对强度，标准化。再乘R2

    解释力度较弱时，数值乘R方会向0压缩
    """
    beta, r2 = ts_simple_regress(high, low, d, lag=0, rettype=[2, 6])
    return ts_zscore(beta, m) * r2
