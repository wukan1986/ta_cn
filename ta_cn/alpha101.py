from .imports_alpha import *


def alpha_001(close, returns, **kwargs):
    """Alpha#1: (rank(Ts_ArgMax(SignedPower(((returns < 0) ? stddev(returns, 20) : close), 2.), 5)) - 0.5)"""
    t1 = IF(returns < 0, stddev(returns, 20), close)
    t2 = ts_argmax(signedpower(t1, 2.), 5)
    return rank(t2) - 0.5  # 将取值范围调整到-0.5~0.5


def alpha_002(open_, close, volume, **kwargs):
    """Alpha#2: (-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6))"""
    t1 = rank(delta(log(volume), 2))  # 成交量变化排名
    t2 = rank(((close - open_) / open_))  # 今日涨幅排名
    return -1 * correlation(t1, t2, 6)


def alpha_003(open_, volume, **kwargs):
    """Alpha#3: (-1 * correlation(rank(open), rank(volume), 10))"""
    # 开盘价与成交量的秩相关系数，10日滚动
    return -1 * correlation(rank(open_), rank(volume), 10)


def alpha_004(low, **kwargs):
    """Alpha#4: (-1 * Ts_Rank(rank(low), 9))"""
    return -1 * ts_rank(rank(low), 9)


def alpha_005(open_, close, vwap, **kwargs):
    """Alpha#5: (rank((open - (sum(vwap, 10) / 10))) * (-1 * abs(rank((close - vwap)))))"""
    return rank((open_ - (sum(vwap, 10) / 10))) * (-1 * abs(rank((close - vwap))))


def alpha_006(open_, volume, **kwargs):
    """Alpha#6: (-1 * correlation(open, volume, 10))"""
    return -1 * correlation(open_, volume, 10)


def alpha_007(close, volume, adv20, **kwargs):
    """Alpha#7: ((adv20 < volume) ? ((-1 * ts_rank(abs(delta(close, 7)), 60)) * sign(delta(close, 7))) : (-1* 1))"""
    t1 = delta(close, 7)
    t2 = (-1 * ts_rank(abs(t1), 60)) * sign(t1)
    return IF(adv20 < volume, t2, -1)


def alpha_008(open_, returns, **kwargs):
    """Alpha#8: (-1 * rank(((sum(open, 5) * sum(returns, 5)) - delay((sum(open, 5) * sum(returns, 5)), 10))))"""
    t1 = sum(open_, 5) * sum(returns, 5)
    t2 = t1 - delay(t1, 10)
    return -1 * rank(t2)


def alpha_009(close, **kwargs):
    """Alpha#9: ((0 < ts_min(delta(close, 1), 5)) ? delta(close, 1) : ((ts_max(delta(close, 1), 5) < 0) ? delta(close, 1) : (-1 * delta(close, 1))))"""
    t1 = delta(close, 1)
    t2 = IF(ts_max(t1, 5) < 0, t1, -1 * t1)
    return IF(0 < ts_min(t1, 5), t1, t2)


def alpha_010(close, **kwargs):
    """Alpha#10: rank(((0 < ts_min(delta(close, 1), 4)) ? delta(close, 1) : ((ts_max(delta(close, 1), 4) < 0) ? delta(close, 1) : (-1 * delta(close, 1)))))"""
    t1 = delta(close, 1)
    t2 = IF(ts_max(t1, 4) < 0, t1, -1 * t1)
    t3 = IF(0 < ts_min(t1, 4), t1, t2)
    return rank(t3)


def alpha_011(close, volume, vwap, **kwargs):
    """Alpha#11: ((rank(ts_max((vwap - close), 3)) + rank(ts_min((vwap - close), 3))) * rank(delta(volume, 3)))"""
    t1 = vwap - close
    t2 = rank(ts_max(t1, 3))
    t3 = rank(ts_min(t1, 3))
    t4 = rank(delta(volume, 3))
    return (t2 + t3) * t4


def alpha_012(close, volume, **kwargs):
    """Alpha#12: (sign(delta(volume, 1)) * (-1 * delta(close, 1)))"""
    t1 = delta(volume, 1)
    t2 = delta(close, 1)
    return sign(t1) * (-1 * t2)


def alpha_013(close, volume, **kwargs):
    """Alpha#13: (-1 * rank(covariance(rank(close), rank(volume), 5)))"""
    t1 = covariance(rank(close), rank(volume), 5)
    return -1 * rank(t1)


def alpha_014(open_, volume, returns, **kwargs):
    """Alpha#14: ((-1 * rank(delta(returns, 3))) * correlation(open, volume, 10))"""
    return (-1 * rank(delta(returns, 3))) * correlation(open_, volume, 10)


def alpha_015(high, volume, **kwargs):
    """Alpha#15: (-1 * sum(rank(correlation(rank(high), rank(volume), 3)), 3))"""
    t1 = correlation(rank(high), rank(volume), 3)
    return -1 * sum(rank(t1), 3)


def alpha_016(high, volume, **kwargs):
    """Alpha#16: (-1 * rank(covariance(rank(high), rank(volume), 5)))"""
    t1 = covariance(rank(high), rank(volume), 5)
    return -1 * rank(t1)


def alpha_017(close, volume, adv20, **kwargs):
    """Alpha#17: (((-1 * rank(ts_rank(close, 10))) * rank(delta(delta(close, 1), 1))) * rank(ts_rank((volume / adv20), 5)))"""
    t1 = rank(ts_rank(close, 10))
    t2 = rank(delta(delta(close, 1), 1))
    t3 = rank(ts_rank((volume / adv20), 5))
    return ((-1 * t1) * t2) * t3


def alpha_018(open_, close, **kwargs):
    """Alpha#18: (-1 * rank(((stddev(abs((close - open)), 5) + (close - open)) + correlation(close, open, 10))))"""
    t1 = close - open_
    t2 = stddev(abs(t1), 5) + t1
    t3 = correlation(close, open_, 10)
    return -1 * rank(t2 + t3)


def alpha_101(open_, high, low, close, **kwargs):
    """Alpha#101: ((close - open) / ((high - low) + .001))"""
    return (close - open_) / ((high - low) + .001)
