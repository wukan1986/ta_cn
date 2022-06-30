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
    t1 = stddev(high, 10)  # 最高价10日标准差
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
    t1 = -1 * delta(close, 7)
    return ts_rank(volume / adv20, 20) * ts_rank(t1, 8)


def alpha_044(high, volume, **kwargs):
    """Alpha#44: (-1 * correlation(high, rank(volume), 5))"""
    return -1 * correlation(high, rank(volume), 5)


def alpha_045(close, volume, **kwargs):
    """Alpha#45: (-1 * ((rank((sum(delay(close, 5), 20) / 20)) * correlation(close, volume, 2)) *
rank(correlation(sum(close, 5), sum(close, 20), 2))))"""
    t1 = sum(delay(close, 5), 20) / 20  # 延后5天的20日移动平均
    t2 = correlation(close, volume, 2)  # 收盘价与成交量的相关系数
    t3 = correlation(sum(close, 5), sum(close, 20), 2)  # 五日收盘价与20日收盘的相关系数
    return -1 * rank(t1) * t2 * rank(t3)


def alpha_046(close, **kwargs):
    """Alpha#46: ((0.25 < (((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10))) ?
(-1 * 1) : (((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < 0) ? 1 :
((-1 * 1) * (close - delay(close, 1)))))"""
    t1 = delay(close, 20) - delay(close, 10)
    t2 = delay(close, 10) - close
    t3 = close - delay(close, 1)
    t4 = (t1 / 10) - (t2 / 10)
    t5 = IF(t4 < 0, 1, -1 * t3)
    return IF(0.25 < t4, -1, t5)


def alpha_047(high, close, volume, vwap, adv20, **kwargs):
    """Alpha#47: ((((rank((1 / close)) * volume) / adv20) * ((high * rank((high - close))) / (sum(high, 5) /
5))) - rank((vwap - delay(vwap, 5))))"""
    t1 = rank(1 / close) * volume / adv20
    t2 = high * rank(high - close)  # 涨得多的权重大
    t3 = sum(high, 5) / 5  # 最高价5日移动平均
    t4 = vwap - delay(vwap, 5)  # vwap的5日动量
    return t1 * (t2 / t3) - rank(t4)


def alpha_048(close, subindustry, **kwargs):
    """Alpha#48: (indneutralize(((correlation(delta(close, 1), delta(delay(close, 1), 1), 250) *
delta(close, 1)) / close), IndClass.subindustry) / sum(((delta(close, 1) / delay(close, 1))^2), 250))"""

    t1 = delta(close, 1)
    t2 = delay(close, 1)
    t3 = correlation(t1, delta(t2, 1), 250)
    t4 = indneutralize(t3 * t1 / close, group=subindustry)
    return t4 / sum(((t1 / t2) ** 2), 250)


def alpha_049(close, **kwargs):
    """Alpha#49: (((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < (-1 *
0.1)) ? 1 : ((-1 * 1) * (close - delay(close, 1))))"""
    t1 = delay(close, 20)
    t2 = delay(close, 10)
    t3 = delay(close, 1)
    t4 = ((t1 - t2) / 10) - ((t2 - close) / 10)
    return IF(t4 < -0.1, 1, t3 - close)


def alpha_050(volume, vwap, **kwargs):
    """Alpha#50: (-1 * ts_max(rank(correlation(rank(volume), rank(vwap), 5)), 5))"""
    t1 = correlation(rank(volume), rank(vwap), 5)  # 秩相关系数
    return -1 * ts_max(rank(t1), 5)


def alpha_051(close, **kwargs):
    """Alpha#51: (((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < (-1 *
0.05)) ? 1 : ((-1 * 1) * (close - delay(close, 1))))"""
    t1 = delay(close, 20)
    t2 = delay(close, 10)
    t3 = delay(close, 1)
    t4 = ((t1 - t2) / 10) - ((t2 - close) / 10)
    return IF((t4 < -0.05), 1, t3 - close)  # 与049区别就是一个值不同


def alpha_052(low, volume, returns, **kwargs):
    """Alpha#52: ((((-1 * ts_min(low, 5)) + delay(ts_min(low, 5), 5)) * rank(((sum(returns, 240) -
sum(returns, 20)) / 220))) * ts_rank(volume, 5))"""
    t1 = ts_min(low, 5)
    t2 = (sum(returns, 240) - sum(returns, 20)) / 220
    t3 = -t1 + delay(t1, 5)
    return t3 * rank(t2) * ts_rank(volume, 5)


def alpha_053(high, low, close, **kwargs):
    """Alpha#53: (-1 * delta((((close - low) - (high - close)) / (close - low)), 9))"""
    t1 = 1 - (high - close) / (close - low)
    return -1 * delta(t1, 9)


def alpha_054(open_, high, low, close, **kwargs):
    """Alpha#54: ((-1 * ((low - close) * (open^5))) / ((low - high) * (close^5)))"""
    return (-1 * ((low - close) * (open_ ** 5))) / ((low - high) * (close ** 5))


def alpha_055(high, low, close, volume, **kwargs):
    """Alpha#55: (-1 * correlation(rank(((close - ts_min(low, 12)) / (ts_max(high, 12) - ts_min(low,
12)))), rank(volume), 6))"""
    t1 = ts_min(low, 12)
    t2 = ts_max(high, 12)
    t3 = (close - t1) / (t2 - t1)
    return -1 * correlation(rank(t3), rank(volume), 6)


def alpha_056(returns, cap, **kwargs):
    """Alpha#56: (0 - (1 * (rank((sum(returns, 10) / sum(sum(returns, 2), 3))) * rank((returns * cap)))))"""
    t1 = sum(returns, 10) / sum(sum(returns, 2), 3)
    return - rank(t1) * rank(returns * cap)


def alpha_057(close, vwap, **kwargs):
    """Alpha#57: (0 - (1 * ((close - vwap) / decay_linear(rank(ts_argmax(close, 30)), 2))))"""
    t1 = decay_linear(rank(ts_argmax(close, 30)), 2)
    return - (close - vwap) / t1


def alpha_058(volume, vwap, sector, **kwargs):
    """Alpha#58: (-1 * Ts_Rank(decay_linear(correlation(IndNeutralize(vwap, IndClass.sector), volume, 3.92795), 7.89291), 5.50322))"""
    t1 = correlation(indneutralize(vwap, group=sector), volume, round(3.92795))
    t2 = decay_linear(t1, round(7.89291))
    return -ts_rank(t2, round(5.50322))


def alpha_059(volume, vwap, industry, **kwargs):
    """Alpha#59: (-1 * Ts_Rank(decay_linear(correlation(IndNeutralize(((vwap * 0.728317) + (vwap * (1 - 0.728317))), IndClass.industry), volume, 4.25197), 16.2289), 8.19648))"""
    t1 = correlation(indneutralize(vwap, group=industry), volume, round(4.25197))
    t2 = decay_linear(t1, round(16.2289))
    return -ts_rank(t2, round(8.19648))  # 与058就是参数不同


def alpha_060(high, low, close, volume, **kwargs):
    """Alpha#60: (0 - (1 * ((2 * scale(rank(((((close - low) - (high - close)) / (high - low)) * volume)))) -
scale(rank(ts_argmax(close, 10))))))"""
    t1 = ts_argmax(close, 10)
    t2 = ((close - low) - (high - close)) / (high - low) * volume
    return scale(rank(t1)) - 2 * scale(rank(t2))


def alpha_061(vwap, adv180, **kwargs):
    """Alpha#61: (rank((vwap - ts_min(vwap, 16.1219))) < rank(correlation(vwap, adv180, 17.9282)))"""
    t1 = vwap - ts_min(vwap, round(16.1219))
    t2 = correlation(vwap, adv180, round(17.9282))
    return rank(t1) - rank(t2) < 0  # 转换了一下


def alpha_062(open_, high, low, vwap, adv20, **kwargs):
    """Alpha#62: ((rank(correlation(vwap, sum(adv20, 22.4101), 9.91009)) < rank(((rank(open) +
rank(open)) < (rank(((high + low) / 2)) + rank(high))))) * -1)"""
    t1 = sum(adv20, round(22.4101))
    t2 = correlation(vwap, t1, round(9.91009))
    t3 = rank(open_) * 2
    t4 = (rank(((high + low) / 2)) + rank(high))
    t5 = rank(t3 - t4 < 0)
    return -(rank(t2) - t5 < 0)


def alpha_063(open_, close, vwap, adv180, industry, **kwargs):
    """Alpha#63: ((rank(decay_linear(delta(IndNeutralize(close, IndClass.industry), 2.25164), 8.22237))
- rank(decay_linear(correlation(((vwap * 0.318108) + (open * (1 - 0.318108))), sum(adv180,
37.2467), 13.557), 12.2883))) * -1)"""
    t1 = delta(indneutralize(close, group=industry), round(2.25164))
    t3 = (vwap * 0.318108) + (open_ * (1 - 0.318108))
    t2 = correlation(t3, sum(adv180, round(37.2467)), round(13.557))
    return rank(decay_linear(t2, round(12.2883))) - rank(decay_linear(t1, round(8.22237)))


def alpha_064(open_, high, low, vwap, adv120, **kwargs):
    """Alpha#64: ((rank(correlation(sum(((open * 0.178404) + (low * (1 - 0.178404))), 12.7054),
sum(adv120, 12.7054), 16.6208)) < rank(delta(((((high + low) / 2) * 0.178404) + (vwap * (1 -
0.178404))), 3.69741))) * -1)"""
    t1 = sum(((open_ * 0.178404) + (low * (1 - 0.178404))), round(12.7054))
    t2 = sum(adv120, round(12.7054))
    t3 = (((high + low) / 2) * 0.178404) + (vwap * (1 - 0.178404))
    t4 = rank(correlation(t1, t2, round(16.6208)))
    t5 = rank(delta(t3, round(3.69741)))
    return -(t4 - t5 < 0)


def alpha_065(open_, vwap, adv60, **kwargs):
    """Alpha#65: ((rank(correlation(((open * 0.00817205) + (vwap * (1 - 0.00817205))), sum(adv60,
8.6911), 6.40374)) < rank((open - ts_min(open, 13.635)))) * -1)"""
    t1 = ((open_ * 0.00817205) + (vwap * (1 - 0.00817205)))
    t2 = sum(adv60, round(8.6911))
    t3 = correlation(t1, t2, round(6.40374))
    t4 = (open_ - ts_min(open_, round(13.635)))
    return -(rank(t3) - rank(t4) < 0)


def alpha_066(open_, high, low, vwap, **kwargs):
    """Alpha#66: ((rank(decay_linear(delta(vwap, 3.51013), 7.23052)) + Ts_Rank(decay_linear(((((low
* 0.96633) + (low * (1 - 0.96633))) - vwap) / (open - ((high + low) / 2))), 11.4157), 6.72611)) * -1)"""
    t1 = delta(vwap, round(3.51013))
    t2 = decay_linear(t1, round(7.23052))
    t3 = (low - vwap) / (open_ - ((high + low) / 2))
    t4 = decay_linear(t3, round(11.4157))
    return -(rank(t2) + ts_rank(t4, round(6.72611)))


def alpha_067(high, vwap, adv20, sector, subindustry, **kwargs):
    """Alpha#67: ((rank((high - ts_min(high, 2.14593)))^rank(correlation(IndNeutralize(vwap,
IndClass.sector), IndNeutralize(adv20, IndClass.subindustry), 6.02936))) * -1)"""
    t1 = high - ts_min(high, round(2.14593))
    t2 = indneutralize(vwap, group=sector)
    t3 = indneutralize(adv20, group=subindustry)
    t4 = correlation(t2, t3, round(6.02936))
    return -(rank(t1) ** rank(t4))


def alpha_068(high, low, close, adv15, **kwargs):
    """Alpha#68: ((Ts_Rank(correlation(rank(high), rank(adv15), 8.91644), 13.9333) <
rank(delta(((close * 0.518371) + (low * (1 - 0.518371))), 1.06157))) * -1)"""
    t1 = correlation(rank(high), rank(adv15), round(8.91644))
    t2 = ((close * 0.518371) + (low * (1 - 0.518371)))
    t3 = delta(t2, round(1.06157))
    return -(ts_rank(t1, round(13.9333)) - rank(t3) < 0)


def alpha_069(close, vwap, adv20, industry, **kwargs):
    """Alpha#69: ((rank(ts_max(delta(IndNeutralize(vwap, IndClass.industry), 2.72412),
4.79344))^Ts_Rank(correlation(((close * 0.490655) + (vwap * (1 - 0.490655))), adv20, 4.92416),
9.0615)) * -1)"""
    t1 = delta(indneutralize(vwap, group=industry), round(2.72412))
    t2 = ts_max(t1, round(4.79344))
    t3 = ((close * 0.490655) + (vwap * (1 - 0.490655)))
    t4 = correlation(t3, adv20, round(4.92416))

    return -(rank(t2) ** ts_rank(t4, round(9.0615)))


def alpha_070(close, vwap, adv50, industry, **kwargs):
    """Alpha#70: ((rank(delta(vwap, 1.29456))^Ts_Rank(correlation(IndNeutralize(close,
IndClass.industry), adv50, 17.8256), 17.9171)) * -1)"""
    t1 = delta(vwap, round(1.29456))
    t2 = indneutralize(close, group=industry)
    t3 = correlation(t2, adv50, round(17.8256))
    return -(rank(t1) ** ts_rank(t3, round(17.9171)))


def alpha_101(open_, high, low, close, **kwargs):
    """Alpha#101: ((close - open) / ((high - low) + .001))"""
    return (close - open_) / ((high - low) + .001)


def alpha_101(open_, high, low, close, **kwargs):
    """Alpha#101: ((close - open) / ((high - low) + .001))"""
    return (close - open_) / ((high - low) + .001)


def alpha_101(open_, high, low, close, **kwargs):
    """Alpha#101: ((close - open) / ((high - low) + .001))"""
    return (close - open_) / ((high - low) + .001)


def alpha_101(open_, high, low, close, **kwargs):
    """Alpha#101: ((close - open) / ((high - low) + .001))"""
    return (close - open_) / ((high - low) + .001)


def alpha_101(open_, high, low, close, **kwargs):
    """Alpha#101: ((close - open) / ((high - low) + .001))"""
    return (close - open_) / ((high - low) + .001)


def alpha_101(open_, high, low, close, **kwargs):
    """Alpha#101: ((close - open) / ((high - low) + .001))"""
    return (close - open_) / ((high - low) + .001)


def alpha_101(open_, high, low, close, **kwargs):
    """Alpha#101: ((close - open) / ((high - low) + .001))"""
    return (close - open_) / ((high - low) + .001)


def alpha_101(open_, high, low, close, **kwargs):
    """Alpha#101: ((close - open) / ((high - low) + .001))"""
    return (close - open_) / ((high - low) + .001)


def alpha_101(open_, high, low, close, **kwargs):
    """Alpha#101: ((close - open) / ((high - low) + .001))"""
    return (close - open_) / ((high - low) + .001)
