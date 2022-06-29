"""alpha101的实现"""
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


def alpha_019(close, returns, **kwargs):
    """Alpha#19: ((-1 * sign(((close - delay(close, 7)) + delta(close, 7)))) * (1 + rank((1 + sum(returns, 250)))))"""
    return (-1 * sign(((close - delay(close, 7)) + delta(close, 7)))) * (1 + rank((1 + sum(returns, 250))))


def alpha_020(open_, high, low, close, **kwargs):
    """Alpha#20: (((-1 * rank((open - delay(high, 1)))) * rank((open - delay(close, 1)))) * rank((open - delay(low, 1))))"""
    return ((-1 * rank((open_ - delay(high, 1)))) * rank((open_ - delay(close, 1)))) * rank((open_ - delay(low, 1)))


def alpha_021(close, volume, adv20, **kwargs):
    """Alpha#21: ((((sum(close, 8) / 8) + stddev(close, 8)) < (sum(close, 2) / 2)) ? (-1 * 1) : (((sum(close, 2) / 2) < ((sum(close, 8) / 8) - stddev(close, 8))) ? 1 : (((1 < (volume / adv20)) || ((volume / adv20) == 1)) ? 1 : (-1 * 1))))"""
    t1 = sum(close, 8) / 8  # 8日移动平均
    t2 = sum(close, 2) / 2  # 2日移动平均
    t3 = t1 + stddev(close, 8)  # 布林上轨
    t4 = t1 - stddev(close, 8)  # 布林下轨
    t5 = IF(((1 < (volume / adv20)) | ((volume / adv20) == 1)), 1, -1)
    t6 = IF(t2 < t4, 1, t5)
    # TODO: 结果是-1 1,需要再验证一下
    return IF(t3 < t2, -1, t6)


def alpha_022(high, close, volume, **kwargs):
    """Alpha#22: (-1 * (delta(correlation(high, volume, 5), 5) * rank(stddev(close, 20))))"""
    return -1 * (delta(correlation(high, volume, 5), 5) * rank(stddev(close, 20)))


def alpha_023(high, **kwargs):
    """Alpha#23: (((sum(high, 20) / 20) < high) ? (-1 * delta(high, 2)) : 0)"""
    t1 = (sum(high, 20) / 20)  # 20日移动平均
    return IF(t1 < high,
              (-1 * delta(high, 2)),
              0)


def alpha_024(close, **kwargs):
    """Alpha#24: ((((delta((sum(close, 100) / 100), 100) / delay(close, 100)) < 0.05) || ((delta((sum(close, 100) / 100), 100) / delay(close, 100)) == 0.05)) ? (-1 * (close - ts_min(close, 100))) : (-1 * delta(close, 3)))"""
    t1 = delay(close, 100)
    t2 = sum(close, 100) / 100
    t3 = delta(t2, 100) / t1
    return IF((t3 <= 0.05),
              (-1 * (close - ts_min(close, 100))),
              (-1 * delta(close, 3)))


def alpha_025(high, close, returns, adv20, vwap, **kwargs):
    """Alpha#25: rank(((((-1 * returns) * adv20) * vwap) * (high - close)))"""
    return rank(((((-1 * returns) * adv20) * vwap) * (high - close)))


def alpha_026(high, volume, **kwargs):
    """Alpha#26: (-1 * ts_max(correlation(ts_rank(volume, 5), ts_rank(high, 5), 5), 3))"""
    return -1 * ts_max(correlation(ts_rank(volume, 5), ts_rank(high, 5), 5), 3)


def alpha_027(volume, vwap, **kwargs):
    """Alpha#27: ((0.5 < rank((sum(correlation(rank(volume), rank(vwap), 6), 2) / 2.0))) ? (-1 * 1) : 1)"""
    return IF((0.5 < rank((sum(correlation(rank(volume), rank(vwap), 6), 2) / 2.0))), -1, 1)


def alpha_028(high, low, close, adv20, **kwargs):
    """Alpha#28: scale(((correlation(adv20, low, 5) + ((high + low) / 2)) - close))"""
    return scale(((correlation(adv20, low, 5) + ((high + low) / 2)) - close))


def alpha_029(close, returns, **kwargs):
    """Alpha#29: (min(product(rank(rank(scale(log(sum(ts_min(rank(rank((-1 * rank(delta((close - 1), 5))))), 2), 1))))), 1), 5) + ts_rank(delay((-1 * returns), 6), 5))"""
    pass
    # return (min(product(rank(rank(scale(log(sum(ts_min(rank(rank((-1 * rank(delta((close - 1), 5))))), 2), 1))))), 1), 5) + ts_rank(delay((-1 * returns), 6), 5))


def alpha_030(close, volume, **kwargs):
    """Alpha#30: (((1.0 - rank(((sign((close - delay(close, 1))) + sign((delay(close, 1) - delay(close, 2)))) +
sign((delay(close, 2) - delay(close, 3)))))) * sum(volume, 5)) / sum(volume, 20))"""
    t1 = sign((close - delay(close, 1)))
    t2 = sign((delay(close, 1) - delay(close, 2)))
    t3 = sign((delay(close, 2) - delay(close, 3)))
    return ((1.0 - rank(t1 + t2 + t3)) * sum(volume, 5)) / sum(volume, 20)


def alpha_031(low, close, adv20, **kwargs):
    """Alpha#31: ((rank(rank(rank(decay_linear((-1 * rank(rank(delta(close, 10)))), 10)))) + rank((-1 *
delta(close, 3)))) + sign(scale(correlation(adv20, low, 12))))"""
    return ((rank(rank(rank(decay_linear((-1 * rank(rank(delta(close, 10)))), 10)))) + rank((-1 *
                                                                                             delta(close, 3)))) + sign(
        scale(correlation(adv20, low, 12))))


def alpha_032(close, vwap, **kwargs):
    """Alpha#32: (scale(((sum(close, 7) / 7) - close)) + (20 * scale(correlation(vwap, delay(close, 5), 230))))"""
    t1 = sum(close, 7) / 7  # 7日移动平均
    t2 = correlation(vwap, delay(close, 5), 230)  # vwap与5天前价格的多日滚动相关系数
    return scale(t1 - close) + (20 * scale(t2))


def alpha_033(open_, close, **kwargs):
    """Alpha#33: rank((-1 * ((1 - (open / close))^1)))"""
    return rank(open_ / close - 1)


def alpha_034(close, returns, **kwargs):
    """Alpha#34: rank(((1 - rank((stddev(returns, 2) / stddev(returns, 5)))) + (1 - rank(delta(close, 1)))))"""
    t1 = stddev(returns, 2) / stddev(returns, 5)  # 收益率的波动之比
    t2 = delta(close, 1)  # 涨幅
    return rank(2 - rank(t1) - rank(t2))


def alpha_035(high, low, close, volume, returns, **kwargs):
    """Alpha#35: ((Ts_Rank(volume, 32) * (1 - Ts_Rank(((close + high) - low), 16))) * (1 - Ts_Rank(returns, 32)))"""
    t1 = ts_rank(volume, 32)
    t2 = ts_rank(close + high - low, 16)
    t3 = ts_rank(returns, 32)
    return t1 * (1 - t2) * (1 - t3)


def alpha_036(open_, close, volume, returns, vwap, adv20, **kwargs):
    """Alpha#36: (((((2.21 * rank(correlation((close - open), delay(volume, 1), 15))) + (0.7 * rank((open
- close)))) + (0.73 * rank(Ts_Rank(delay((-1 * returns), 6), 5)))) + rank(abs(correlation(vwap,
adv20, 6)))) + (0.6 * rank((((sum(close, 200) / 200) - open) * (close - open)))))"""
    return (((((2.21 * rank(correlation((close - open_), delay(volume, 1), 15))) + (0.7 * rank((open_
                                                                                                - close)))) + (
                      0.73 * rank(ts_rank(delay((-1 * returns), 6), 5)))) + rank(abs(correlation(vwap,
                                                                                                 adv20, 6)))) + (
                    0.6 * rank((((sum(close, 200) / 200) - open_) * (close - open_)))))


def alpha_037(open_, close, **kwargs):
    """Alpha#37: (rank(correlation(delay((open - close), 1), close, 200)) + rank((open - close)))"""
    t1 = open_ - close  # 当日跌幅
    t2 = delay(t1, 1)  # 昨日跌幅
    t3 = correlation(t2, close, 200)  # 昨日跌幅与今日价格的相关系数
    return rank(t3) + rank(t1)


def alpha_038(open_, close, **kwargs):
    """Alpha#38: ((-1 * rank(Ts_Rank(close, 10))) * rank((close / open)))"""
    t1 = ts_rank(close, 10)
    t2 = close / open_
    return -1 * rank(t1) * rank(t2)


def alpha_039(close, volume, returns, adv20, **kwargs):
    """Alpha#39: ((-1 * rank((delta(close, 7) * (1 - rank(decay_linear((volume / adv20), 9)))))) * (1 +
rank(sum(returns, 250))))"""
    t1 = delta(close, 7)
    t2 = decay_linear((volume / adv20), 9)
    t3 = sum(returns, 250)
    return -1 * rank(t1 * (1 - rank(t2))) * (1 + rank(t3))


def alpha_040(high, volume, **kwargs):
    """Alpha#40: ((-1 * rank(stddev(high, 10))) * correlation(high, volume, 10))"""
    t1 = stddev(high, 10)
    t2 = correlation(high, volume, 10)
    return -1 * rank(t1) * t2


def alpha_041(high, low, vwap, **kwargs):
    """Alpha#41: (((high * low)^0.5) - vwap)"""
    return ((high * low) ** 0.5) - vwap


def alpha_042(close, vwap, **kwargs):
    """Alpha#42: (rank((vwap - close)) / rank((vwap + close)))"""
    return rank((vwap - close)) / rank((vwap + close))


def alpha_043(close, volume, adv20, **kwargs):
    """Alpha#43: (ts_rank((volume / adv20), 20) * ts_rank((-1 * delta(close, 7)), 8))"""
    return ts_rank(volume / adv20, 20) * ts_rank((-1 * delta(close, 7)), 8)


def alpha_044(high, volume, **kwargs):
    """Alpha#44: (-1 * correlation(high, rank(volume), 5))"""
    return -1 * correlation(high, rank(volume), 5)


def alpha_045(close, volume, **kwargs):
    """Alpha#45: (-1 * ((rank((sum(delay(close, 5), 20) / 20)) * correlation(close, volume, 2)) *
rank(correlation(sum(close, 5), sum(close, 20), 2))))"""
    return (-1 * ((rank((sum(delay(close, 5), 20) / 20)) * correlation(close, volume, 2)) *
                  rank(correlation(sum(close, 5), sum(close, 20), 2))))


def alpha_046(close, **kwargs):
    """Alpha#46: ((0.25 < (((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10))) ?
(-1 * 1) : (((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < 0) ? 1 :
((-1 * 1) * (close - delay(close, 1)))))"""
    pass


def alpha_047(high, close, volume, vwap, adv20, **kwargs):
    """Alpha#47: ((((rank((1 / close)) * volume) / adv20) * ((high * rank((high - close))) / (sum(high, 5) /
5))) - rank((vwap - delay(vwap, 5))))"""
    return ((((rank((1 / close)) * volume) / adv20) * ((high * rank((high - close))) / (sum(high, 5) / 5))) - rank(
        (vwap - delay(vwap, 5))))


def alpha_101(open_, high, low, close, **kwargs):
    """Alpha#101: ((close - open) / ((high - low) + .001))"""
    return (close - open_) / ((high - low) + .001)
