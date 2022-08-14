"""alpha101的实现

不做优化，直接复制。主要是防止在别的地方的代码优化时搞错，
在这里不做优化，只做转换，所以出错的概率小

1. ?:三元表达式要改成 IF()
2. ||改成|
3. ^改成**
4 <改成LessThan
"""
from ..imports_wq import *


def alpha_001(close, returns, **kwargs):
    """Alpha#1: (rank(Ts_ArgMax(SignedPower(((returns < 0) ? stddev(returns, 20) : close), 2.), 5)) - 0.5)"""
    return (rank(Ts_ArgMax(SignedPower(IF((returns < 0), stddev(returns, 20), close), 2.), 5)) - 0.5)


def alpha_002(open, close, volume, **kwargs):
    """Alpha#2: (-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6))"""
    return (-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6))


def alpha_003(open, volume, **kwargs):
    """Alpha#3: (-1 * correlation(rank(open), rank(volume), 10))"""
    return (-1 * correlation(rank(open), rank(volume), 10))


def alpha_004(low, **kwargs):
    """Alpha#4: (-1 * Ts_Rank(rank(low), 9))"""
    return (-1 * Ts_Rank(rank(low), 9))


def alpha_005(open, close, vwap, **kwargs):
    """Alpha#5: (rank((open - (sum(vwap, 10) / 10))) * (-1 * abs(rank((close - vwap)))))"""
    return (rank((open - (sum(vwap, 10) / 10))) * (-1 * abs(rank((close - vwap)))))


def alpha_006(open, volume, **kwargs):
    """Alpha#6: (-1 * correlation(open, volume, 10))"""
    return (-1 * correlation(open, volume, 10))


def alpha_007(close, volume, adv20, **kwargs):
    """Alpha#7: ((adv20 < volume) ? ((-1 * ts_rank(abs(delta(close, 7)), 60)) * sign(delta(close, 7))) : (-1* 1))"""
    return IF((adv20 < volume), ((-1 * ts_rank(abs(delta(close, 7)), 60)) * sign(delta(close, 7))), (-1 * 1))


def alpha_008(open, returns, **kwargs):
    """Alpha#8: (-1 * rank(((sum(open, 5) * sum(returns, 5)) - delay((sum(open, 5) * sum(returns, 5)), 10))))"""
    return (-1 * rank(((sum(open, 5) * sum(returns, 5)) - delay((sum(open, 5) * sum(returns, 5)), 10))))


def alpha_009(close, **kwargs):
    """Alpha#9: ((0 < ts_min(delta(close, 1), 5)) ? delta(close, 1) : ((ts_max(delta(close, 1), 5) < 0) ? delta(close, 1) : (-1 * delta(close, 1))))"""
    return IF((0 < ts_min(delta(close, 1), 5)), delta(close, 1),
              IF((ts_max(delta(close, 1), 5) < 0), delta(close, 1), (-1 * delta(close, 1))))


def alpha_010(close, **kwargs):
    """Alpha#10: rank(((0 < ts_min(delta(close, 1), 4)) ? delta(close, 1) : ((ts_max(delta(close, 1), 4) < 0) ? delta(close, 1) : (-1 * delta(close, 1)))))"""
    return rank(IF((0 < ts_min(delta(close, 1), 4)), delta(close, 1),
                   IF((ts_max(delta(close, 1), 4) < 0), delta(close, 1), (-1 * delta(close, 1)))))


def alpha_011(close, volume, vwap, **kwargs):
    """Alpha#11: ((rank(ts_max((vwap - close), 3)) + rank(ts_min((vwap - close), 3))) * rank(delta(volume, 3)))"""
    return ((rank(ts_max((vwap - close), 3)) + rank(ts_min((vwap - close), 3))) * rank(delta(volume, 3)))


def alpha_012(close, volume, **kwargs):
    """Alpha#12: (sign(delta(volume, 1)) * (-1 * delta(close, 1)))"""
    return (sign(delta(volume, 1)) * (-1 * delta(close, 1)))


def alpha_013(close, volume, **kwargs):
    """Alpha#13: (-1 * rank(covariance(rank(close), rank(volume), 5)))"""
    return (-1 * rank(covariance(rank(close), rank(volume), 5)))


def alpha_014(open, volume, returns, **kwargs):
    """Alpha#14: ((-1 * rank(delta(returns, 3))) * correlation(open, volume, 10))"""
    return ((-1 * rank(delta(returns, 3))) * correlation(open, volume, 10))


def alpha_015(high, volume, **kwargs):
    """Alpha#15: (-1 * sum(rank(correlation(rank(high), rank(volume), 3)), 3))"""
    return (-1 * sum(rank(correlation(rank(high), rank(volume), 3)), 3))


def alpha_016(high, volume, **kwargs):
    """Alpha#16: (-1 * rank(covariance(rank(high), rank(volume), 5)))"""
    return (-1 * rank(covariance(rank(high), rank(volume), 5)))


def alpha_017(close, volume, adv20, **kwargs):
    """Alpha#17: (((-1 * rank(ts_rank(close, 10))) * rank(delta(delta(close, 1), 1))) * rank(ts_rank((volume / adv20), 5)))"""
    return (((-1 * rank(ts_rank(close, 10))) * rank(delta(delta(close, 1), 1))) * rank(ts_rank((volume / adv20), 5)))


def alpha_018(open, close, **kwargs):
    """Alpha#18: (-1 * rank(((stddev(abs((close - open)), 5) + (close - open)) + correlation(close, open, 10))))"""
    return (-1 * rank(((stddev(abs((close - open)), 5) + (close - open)) + correlation(close, open, 10))))


def alpha_019(close, returns, **kwargs):
    """Alpha#19: ((-1 * sign(((close - delay(close, 7)) + delta(close, 7)))) * (1 + rank((1 + sum(returns, 250)))))"""
    return ((-1 * sign(((close - delay(close, 7)) + delta(close, 7)))) * (1 + rank((1 + sum(returns, 250)))))


def alpha_020(open, high, low, close, **kwargs):
    """Alpha#20: (((-1 * rank((open - delay(high, 1)))) * rank((open - delay(close, 1)))) * rank((open - delay(low, 1))))"""
    return (((-1 * rank((open - delay(high, 1)))) * rank((open - delay(close, 1)))) * rank((open - delay(low, 1))))


def alpha_021(close, volume, adv20, **kwargs):
    """Alpha#21: ((((sum(close, 8) / 8) + stddev(close, 8)) < (sum(close, 2) / 2)) ? (-1 * 1) : (((sum(close, 2) / 2) < ((sum(close, 8) / 8) - stddev(close, 8))) ? 1 : (((1 < (volume / adv20)) || ((volume / adv20) == 1)) ? 1 : (-1 * 1))))"""
    return IF((((sum(close, 8) / 8) + stddev(close, 8)) < (sum(close, 2) / 2)), (-1 * 1),
              IF(((sum(close, 2) / 2) < ((sum(close, 8) / 8) - stddev(close, 8))), 1,
                 IF(((1 < (volume / adv20)) | ((volume / adv20) == 1)), 1, (-1 * 1))))


def alpha_022(high, close, volume, **kwargs):
    """Alpha#22: (-1 * (delta(correlation(high, volume, 5), 5) * rank(stddev(close, 20))))"""
    return (-1 * (delta(correlation(high, volume, 5), 5) * rank(stddev(close, 20))))


def alpha_023(high, **kwargs):
    """Alpha#23: (((sum(high, 20) / 20) < high) ? (-1 * delta(high, 2)) : 0)"""
    return IF(((sum(high, 20) / 20) < high), (-1 * delta(high, 2)), 0)


def alpha_024(close, **kwargs):
    """Alpha#24: ((((delta((sum(close, 100) / 100), 100) / delay(close, 100)) < 0.05) || ((delta((sum(close, 100) / 100), 100) / delay(close, 100)) == 0.05)) ? (-1 * (close - ts_min(close, 100))) : (-1 * delta(close, 3)))"""
    return IF((((delta((sum(close, 100) / 100), 100) / delay(close, 100)) < 0.05) | (
            (delta((sum(close, 100) / 100), 100) / delay(close, 100)) == 0.05)),
              (-1 * (close - ts_min(close, 100))), (-1 * delta(close, 3)))


def alpha_025(high, close, returns, adv20, vwap, **kwargs):
    """Alpha#25: rank(((((-1 * returns) * adv20) * vwap) * (high - close)))"""
    return rank(((((-1 * returns) * adv20) * vwap) * (high - close)))


def alpha_026(high, volume, **kwargs):
    """Alpha#26: (-1 * ts_max(correlation(ts_rank(volume, 5), ts_rank(high, 5), 5), 3))"""
    return (-1 * ts_max(correlation(ts_rank(volume, 5), ts_rank(high, 5), 5), 3))


def alpha_027(volume, vwap, **kwargs):
    """Alpha#27: ((0.5 < rank((sum(correlation(rank(volume), rank(vwap), 6), 2) / 2.0))) ? (-1 * 1) : 1)"""
    return IF((0.5 < rank((sum(correlation(rank(volume), rank(vwap), 6), 2) / 2.0))), (-1 * 1), 1)


def alpha_028(high, low, close, adv20, **kwargs):
    """Alpha#28: scale(((correlation(adv20, low, 5) + ((high + low) / 2)) - close))"""
    return scale(((correlation(adv20, low, 5) + ((high + low) / 2)) - close), 1)


def alpha_029(close, returns, **kwargs):
    """Alpha#29: (min(product(rank(rank(scale(log(sum(ts_min(rank(rank((-1 * rank(delta((close - 1), 5))))), 2), 1))))), 1), 5) + ts_rank(delay((-1 * returns), 6), 5))"""
    return (min(
        product(rank(rank(scale(log(sum(ts_min(rank(rank((-1 * rank(delta((close - 1), 5))))), 2), 1)), 1))), 1),
        5) + ts_rank(delay((-1 * returns), 6), 5))


def alpha_030(close, volume, **kwargs):
    """Alpha#30: (((1.0 - rank(((sign((close - delay(close, 1))) + sign((delay(close, 1) - delay(close, 2)))) +
sign((delay(close, 2) - delay(close, 3)))))) * sum(volume, 5)) / sum(volume, 20))"""
    return (((1.0 - rank(((sign((close - delay(close, 1))) + sign((delay(close, 1) - delay(close, 2)))) +
                          sign((delay(close, 2) - delay(close, 3)))))) * sum(volume, 5)) / sum(volume, 20))


def alpha_031(low, close, adv20, **kwargs):
    """Alpha#31: ((rank(rank(rank(decay_linear((-1 * rank(rank(delta(close, 10)))), 10)))) + rank((-1 *
delta(close, 3)))) + sign(scale(correlation(adv20, low, 12))))"""
    return ((rank(rank(rank(decay_linear((-1 * rank(rank(delta(close, 10)))), 10)))) + rank((-1 *
                                                                                             delta(close, 3)))) + sign(
        scale(correlation(adv20, low, 12), 1)))


def alpha_032(close, vwap, **kwargs):
    """Alpha#32: (scale(((sum(close, 7) / 7) - close)) + (20 * scale(correlation(vwap, delay(close, 5), 230))))"""
    return (scale(((sum(close, 7) / 7) - close), 1) + (20 * scale(correlation(vwap, delay(close, 5), 230), 1)))


def alpha_033(open, close, **kwargs):
    """Alpha#33: rank((-1 * ((1 - (open / close))^1)))"""
    return rank((-1 * ((1 - (open / close)) ** 1)))


def alpha_034(close, returns, **kwargs):
    """Alpha#34: rank(((1 - rank((stddev(returns, 2) / stddev(returns, 5)))) + (1 - rank(delta(close, 1)))))"""
    return rank(((1 - rank((stddev(returns, 2) / stddev(returns, 5)))) + (1 - rank(delta(close, 1)))))


def alpha_035(high, low, close, volume, returns, **kwargs):
    """Alpha#35: ((Ts_Rank(volume, 32) * (1 - Ts_Rank(((close + high) - low), 16))) * (1 - Ts_Rank(returns, 32)))"""
    return ((Ts_Rank(volume, 32) * (1 - Ts_Rank(((close + high) - low), 16))) * (1 - Ts_Rank(returns, 32)))


def alpha_036(open, close, volume, returns, vwap, adv20, **kwargs):
    """Alpha#36: (((((2.21 * rank(correlation((close - open), delay(volume, 1), 15))) + (0.7 * rank((open
- close)))) + (0.73 * rank(Ts_Rank(delay((-1 * returns), 6), 5)))) + rank(abs(correlation(vwap,
adv20, 6)))) + (0.6 * rank((((sum(close, 200) / 200) - open) * (close - open)))))"""
    return (((((2.21 * rank(correlation((close - open), delay(volume, 1), 15))) + (0.7 * rank((open
                                                                                               - close)))) + (
                      0.73 * rank(Ts_Rank(delay((-1 * returns), 6), 5)))) + rank(abs(correlation(vwap,
                                                                                                 adv20, 6)))) + (
                    0.6 * rank((((sum(close, 200) / 200) - open) * (close - open)))))


def alpha_037(open, close, **kwargs):
    """Alpha#37: (rank(correlation(delay((open - close), 1), close, 200)) + rank((open - close)))"""
    return (rank(correlation(delay((open - close), 1), close, 200)) + rank((open - close)))


def alpha_038(open, close, **kwargs):
    """Alpha#38: ((-1 * rank(Ts_Rank(close, 10))) * rank((close / open)))"""
    return ((-1 * rank(Ts_Rank(close, 10))) * rank((close / open)))


def alpha_039(close, volume, returns, adv20, **kwargs):
    """Alpha#39: ((-1 * rank((delta(close, 7) * (1 - rank(decay_linear((volume / adv20), 9)))))) * (1 +
rank(sum(returns, 250))))"""
    return ((-1 * rank((delta(close, 7) * (1 - rank(decay_linear((volume / adv20), 9)))))) * (1 +
                                                                                              rank(sum(returns, 250))))


def alpha_040(high, volume, **kwargs):
    """Alpha#40: ((-1 * rank(stddev(high, 10))) * correlation(high, volume, 10))"""
    return ((-1 * rank(stddev(high, 10))) * correlation(high, volume, 10))


def alpha_041(high, low, vwap, **kwargs):
    """Alpha#41: (((high * low)^0.5) - vwap)"""
    return (((high * low) ** 0.5) - vwap)


def alpha_042(close, vwap, **kwargs):
    """Alpha#42: (rank((vwap - close)) / rank((vwap + close)))"""
    return (rank((vwap - close)) / rank((vwap + close)))


def alpha_043(close, volume, adv20, **kwargs):
    """Alpha#43: (ts_rank((volume / adv20), 20) * ts_rank((-1 * delta(close, 7)), 8))"""
    return (ts_rank((volume / adv20), 20) * ts_rank((-1 * delta(close, 7)), 8))


def alpha_044(high, volume, **kwargs):
    """Alpha#44: (-1 * correlation(high, rank(volume), 5))"""
    return (-1 * correlation(high, rank(volume), 5))


def alpha_045(close, volume, **kwargs):
    """Alpha#45: (-1 * ((rank((sum(delay(close, 5), 20) / 20)) * correlation(close, volume, 2)) *
rank(correlation(sum(close, 5), sum(close, 20), 2))))"""
    return (-1 * ((rank((sum(delay(close, 5), 20) / 20)) * correlation(close, volume, 2)) *
                  rank(correlation(sum(close, 5), sum(close, 20), 2))))


def alpha_046(close, **kwargs):
    """Alpha#46: ((0.25 < (((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10))) ?
(-1 * 1) : (((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < 0) ? 1 :
((-1 * 1) * (close - delay(close, 1)))))"""
    return IF((0.25 < (((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10))),
              (-1 * 1), IF(((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < 0), 1,
                           ((-1 * 1) * (close - delay(close, 1)))))


def alpha_047(high, close, volume, vwap, adv20, **kwargs):
    """Alpha#47: ((((rank((1 / close)) * volume) / adv20) * ((high * rank((high - close))) / (sum(high, 5) /
5))) - rank((vwap - delay(vwap, 5))))"""
    return ((((rank((1 / close)) * volume) / adv20) * ((high * rank((high - close))) / (sum(high, 5) /
                                                                                        5))) - rank(
        (vwap - delay(vwap, 5))))


def alpha_048(close, subindustry, **kwargs):
    """Alpha#48: (indneutralize(((correlation(delta(close, 1), delta(delay(close, 1), 1), 250) *
delta(close, 1)) / close), IndClass.subindustry) / sum(((delta(close, 1) / delay(close, 1))^2), 250))"""
    return (indneutralize(((correlation(delta(close, 1), delta(delay(close, 1), 1), 250) *
                            delta(close, 1)) / close), group=subindustry) / sum(
        ((delta(close, 1) / delay(close, 1)) ** 2), 250))


def alpha_049(close, **kwargs):
    """Alpha#49: (((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < (-1 *
0.1)) ? 1 : ((-1 * 1) * (close - delay(close, 1))))"""
    return IF(((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < (-1 *
                                                                                                     0.1)), 1,
              ((-1 * 1) * (close - delay(close, 1))))


def alpha_050(volume, vwap, **kwargs):
    """Alpha#50: (-1 * ts_max(rank(correlation(rank(volume), rank(vwap), 5)), 5))"""
    return (-1 * ts_max(rank(correlation(rank(volume), rank(vwap), 5)), 5))


def alpha_051(close, **kwargs):
    """Alpha#51: (((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < (-1 *
0.05)) ? 1 : ((-1 * 1) * (close - delay(close, 1))))"""
    return IF(((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < (-1 *
                                                                                                     0.05)), 1,
              ((-1 * 1) * (close - delay(close, 1))))


def alpha_052(low, volume, returns, **kwargs):
    """Alpha#52: ((((-1 * ts_min(low, 5)) + delay(ts_min(low, 5), 5)) * rank(((sum(returns, 240) -
sum(returns, 20)) / 220))) * ts_rank(volume, 5))"""
    return ((((-1 * ts_min(low, 5)) + delay(ts_min(low, 5), 5)) * rank(((sum(returns, 240) -
                                                                         sum(returns, 20)) / 220))) * ts_rank(volume,
                                                                                                              5))


def alpha_053(high, low, close, **kwargs):
    """Alpha#53: (-1 * delta((((close - low) - (high - close)) / (close - low)), 9))"""
    return (-1 * delta((((close - low) - (high - close)) / (close - low)), 9))


def alpha_054(open, high, low, close, **kwargs):
    """Alpha#54: ((-1 * ((low - close) * (open^5))) / ((low - high) * (close^5)))"""
    return ((-1 * ((low - close) * (open ** 5))) / ((low - high) * (close ** 5)))


def alpha_055(high, low, close, volume, **kwargs):
    """Alpha#55: (-1 * correlation(rank(((close - ts_min(low, 12)) / (ts_max(high, 12) - ts_min(low,
12)))), rank(volume), 6))"""
    return (-1 * correlation(rank(((close - ts_min(low, 12)) / (ts_max(high, 12) - ts_min(low,
                                                                                          12)))), rank(volume), 6))


def alpha_056(returns, cap, **kwargs):
    """Alpha#56: (0 - (1 * (rank((sum(returns, 10) / sum(sum(returns, 2), 3))) * rank((returns * cap)))))"""
    return (0 - (1 * (rank((sum(returns, 10) / sum(sum(returns, 2), 3))) * rank((returns * cap)))))


def alpha_057(close, vwap, **kwargs):
    """Alpha#57: (0 - (1 * ((close - vwap) / decay_linear(rank(ts_argmax(close, 30)), 2))))"""
    return (0 - (1 * ((close - vwap) / decay_linear(rank(ts_argmax(close, 30)), 2))))


def alpha_058(volume, vwap, sector, **kwargs):
    """Alpha#58: (-1 * Ts_Rank(decay_linear(correlation(IndNeutralize(vwap, IndClass.sector), volume, 3.92795), 7.89291), 5.50322))"""
    return (-1 * Ts_Rank(decay_linear(correlation(IndNeutralize(vwap, group=sector), volume, 3.92795), 7.89291),
                         5.50322))


def alpha_059(volume, vwap, industry, **kwargs):
    """Alpha#59: (-1 * Ts_Rank(decay_linear(correlation(IndNeutralize(((vwap * 0.728317) + (vwap * (1 - 0.728317))), IndClass.industry), volume, 4.25197), 16.2289), 8.19648))"""
    return (-1 * Ts_Rank(decay_linear(
        correlation(IndNeutralize(((vwap * 0.728317) + (vwap * (1 - 0.728317))), group=industry), volume, 4.25197),
        16.2289), 8.19648))


def alpha_060(high, low, close, volume, **kwargs):
    """Alpha#60: (0 - (1 * ((2 * scale(rank(((((close - low) - (high - close)) / (high - low)) * volume)))) -
scale(rank(ts_argmax(close, 10))))))"""
    return (0 - (1 * ((2 * scale(rank(((((close - low) - (high - close)) / (high - low)) * volume)), 1)) -
                      scale(rank(ts_argmax(close, 10)), 1))))


def alpha_061(vwap, adv180, **kwargs):
    """Alpha#61: (rank((vwap - ts_min(vwap, 16.1219))) < rank(correlation(vwap, adv180, 17.9282)))"""
    return LessThan(rank((vwap - ts_min(vwap, 16.1219))), rank(correlation(vwap, adv180, 17.9282)))


def alpha_062(open, high, low, vwap, adv20, **kwargs):
    """Alpha#62: ((rank(correlation(vwap, sum(adv20, 22.4101), 9.91009)) < rank(((rank(open) +
rank(open)) < (rank(((high + low) / 2)) + rank(high))))) * -1)"""
    return (LessThan(rank(correlation(vwap, sum(adv20, 22.4101), 9.91009)),
                     rank(((rank(open) + rank(open)) < (rank(((high + low) / 2)) + rank(high))))) * -1)


def alpha_063(open, close, vwap, adv180, industry, **kwargs):
    """Alpha#63: ((rank(decay_linear(delta(IndNeutralize(close, IndClass.industry), 2.25164), 8.22237))
- rank(decay_linear(correlation(((vwap * 0.318108) + (open * (1 - 0.318108))), sum(adv180,
37.2467), 13.557), 12.2883))) * -1)"""
    return ((rank(decay_linear(delta(IndNeutralize(close, group=industry), 2.25164), 8.22237))
             - rank(decay_linear(correlation(((vwap * 0.318108) + (open * (1 - 0.318108))), sum(adv180,
                                                                                                37.2467), 13.557),
                                 12.2883))) * -1)


def alpha_064(open, high, low, vwap, adv120, **kwargs):
    """Alpha#64: ((rank(correlation(sum(((open * 0.178404) + (low * (1 - 0.178404))), 12.7054),
sum(adv120, 12.7054), 16.6208)) < rank(delta(((((high + low) / 2) * 0.178404) + (vwap * (1 -
0.178404))), 3.69741))) * -1)"""
    return (LessThan(rank(correlation(sum(((open * 0.178404) + (low * (1 - 0.178404))), 12.7054),
                                      sum(adv120, 12.7054), 16.6208)),
                     rank(delta(((((high + low) / 2) * 0.178404) + (vwap * (1 -
                                                                            0.178404))), 3.69741))) * -1)


def alpha_065(open, vwap, adv60, **kwargs):
    """Alpha#65: ((rank(correlation(((open * 0.00817205) + (vwap * (1 - 0.00817205))), sum(adv60,
8.6911), 6.40374)) < rank((open - ts_min(open, 13.635)))) * -1)"""
    return (LessThan(rank(correlation(((open * 0.00817205) + (vwap * (1 - 0.00817205))), sum(adv60,
                                                                                             8.6911), 6.40374)),
                     rank((open - ts_min(open, 13.635)))) * -1)


def alpha_066(open, high, low, vwap, **kwargs):
    """Alpha#66: ((rank(decay_linear(delta(vwap, 3.51013), 7.23052)) + Ts_Rank(decay_linear(((((low
* 0.96633) + (low * (1 - 0.96633))) - vwap) / (open - ((high + low) / 2))), 11.4157), 6.72611)) * -1)"""
    return ((rank(decay_linear(delta(vwap, 3.51013), 7.23052)) + Ts_Rank(decay_linear(((((low
                                                                                          * 0.96633) + (low * (
            1 - 0.96633))) - vwap) / (open - ((high + low) / 2))), 11.4157), 6.72611)) * -1)


def alpha_067(high, vwap, adv20, sector, subindustry, **kwargs):
    """Alpha#67: ((rank((high - ts_min(high, 2.14593)))^rank(correlation(IndNeutralize(vwap,
IndClass.sector), IndNeutralize(adv20, IndClass.subindustry), 6.02936))) * -1)"""
    return ((rank((high - ts_min(high, 2.14593))) ** rank(correlation(IndNeutralize(vwap,
                                                                                    group=sector),
                                                                      IndNeutralize(adv20, group=subindustry),
                                                                      6.02936))) * -1)


def alpha_068(high, low, close, adv15, **kwargs):
    """Alpha#68: ((Ts_Rank(correlation(rank(high), rank(adv15), 8.91644), 13.9333) <
rank(delta(((close * 0.518371) + (low * (1 - 0.518371))), 1.06157))) * -1)"""
    return (LessThan(Ts_Rank(correlation(rank(high), rank(adv15), 8.91644), 13.9333),
                     rank(delta(((close * 0.518371) + (low * (1 - 0.518371))), 1.06157))) * -1)


def alpha_069(close, vwap, adv20, industry, **kwargs):
    """Alpha#69: ((rank(ts_max(delta(IndNeutralize(vwap, IndClass.industry), 2.72412),
4.79344))^Ts_Rank(correlation(((close * 0.490655) + (vwap * (1 - 0.490655))), adv20, 4.92416),
9.0615)) * -1)"""
    return ((rank(ts_max(delta(IndNeutralize(vwap, group=industry), 2.72412),
                         4.79344)) ** Ts_Rank(
        correlation(((close * 0.490655) + (vwap * (1 - 0.490655))), adv20, 4.92416),
        9.0615)) * -1)


def alpha_070(close, vwap, adv50, industry, **kwargs):
    """Alpha#70: ((rank(delta(vwap, 1.29456))^Ts_Rank(correlation(IndNeutralize(close,
IndClass.industry), adv50, 17.8256), 17.9171)) * -1)"""
    return ((rank(delta(vwap, 1.29456)) ** Ts_Rank(correlation(IndNeutralize(close,
                                                                             group=industry), adv50, 17.8256),
                                                   17.9171)) * -1)


def alpha_071(open, low, close, vwap, adv180, **kwargs):
    """Alpha#71: max(Ts_Rank(decay_linear(correlation(Ts_Rank(close, 3.43976), Ts_Rank(adv180,
12.0647), 18.0175), 4.20501), 15.6948), Ts_Rank(decay_linear((rank(((low + open) - (vwap +
vwap)))^2), 16.4662), 4.4388))"""
    return max(Ts_Rank(decay_linear(correlation(Ts_Rank(close, 3.43976), Ts_Rank(adv180,
                                                                                 12.0647), 18.0175), 4.20501), 15.6948),
               Ts_Rank(decay_linear((rank(((low + open) - (vwap +
                                                           vwap))) ** 2), 16.4662), 4.4388))


def alpha_072(high, low, volume, vwap, adv40, **kwargs):
    """Alpha#72: (rank(decay_linear(correlation(((high + low) / 2), adv40, 8.93345), 10.1519)) /
rank(decay_linear(correlation(Ts_Rank(vwap, 3.72469), Ts_Rank(volume, 18.5188), 6.86671),
2.95011)))"""
    return (rank(decay_linear(correlation(((high + low) / 2), adv40, 8.93345), 10.1519)) /
            rank(decay_linear(correlation(Ts_Rank(vwap, 3.72469), Ts_Rank(volume, 18.5188), 6.86671),
                              2.95011)))


def alpha_073(open, low, vwap, **kwargs):
    """Alpha#73: (max(rank(decay_linear(delta(vwap, 4.72775), 2.91864)),
Ts_Rank(decay_linear(((delta(((open * 0.147155) + (low * (1 - 0.147155))), 2.03608) / ((open *
0.147155) + (low * (1 - 0.147155)))) * -1), 3.33829), 16.7411)) * -1)"""
    return (max(rank(decay_linear(delta(vwap, 4.72775), 2.91864)),
                Ts_Rank(decay_linear(((delta(((open * 0.147155) + (low * (1 - 0.147155))), 2.03608) / ((open *
                                                                                                        0.147155) + (
                                                                                                               low * (
                                                                                                               1 - 0.147155)))) * -1),
                                     3.33829), 16.7411)) * -1)


def alpha_074(high, close, volume, vwap, adv30, **kwargs):
    """Alpha#74: ((rank(correlation(close, sum(adv30, 37.4843), 15.1365)) <
rank(correlation(rank(((high * 0.0261661) + (vwap * (1 - 0.0261661)))), rank(volume), 11.4791)))
* -1)"""
    return (LessThan(rank(correlation(close, sum(adv30, 37.4843), 15.1365)),
                     rank(correlation(rank(((high * 0.0261661) + (vwap * (1 - 0.0261661)))), rank(volume), 11.4791)))
            * -1)


def alpha_075(low, volume, vwap, adv50, **kwargs):
    """Alpha#75: (rank(correlation(vwap, volume, 4.24304)) < rank(correlation(rank(low), rank(adv50),
12.4413)))"""
    return (rank(correlation(vwap, volume, 4.24304)) < rank(correlation(rank(low), rank(adv50),
                                                                        12.4413)))


def alpha_076(low, vwap, adv81, sector, **kwargs):
    """Alpha#76: (max(rank(decay_linear(delta(vwap, 1.24383), 11.8259)),
Ts_Rank(decay_linear(Ts_Rank(correlation(IndNeutralize(low, IndClass.sector), adv81,
8.14941), 19.569), 17.1543), 19.383)) * -1)"""
    return (max(rank(decay_linear(delta(vwap, 1.24383), 11.8259)),
                Ts_Rank(decay_linear(Ts_Rank(correlation(IndNeutralize(low, group=sector), adv81,
                                                         8.14941), 19.569), 17.1543), 19.383)) * -1)


def alpha_077(high, low, vwap, adv40, **kwargs):
    """Alpha#77: min(rank(decay_linear(((((high + low) / 2) + high) - (vwap + high)), 20.0451)),
rank(decay_linear(correlation(((high + low) / 2), adv40, 3.1614), 5.64125)))"""
    return min(rank(decay_linear(((((high + low) / 2) + high) - (vwap + high)), 20.0451)),
               rank(decay_linear(correlation(((high + low) / 2), adv40, 3.1614), 5.64125)))


def alpha_078(low, volume, vwap, adv40, **kwargs):
    """Alpha#78: (rank(correlation(sum(((low * 0.352233) + (vwap * (1 - 0.352233))), 19.7428),
sum(adv40, 19.7428), 6.83313))^rank(correlation(rank(vwap), rank(volume), 5.77492)))"""
    return (rank(correlation(sum(((low * 0.352233) + (vwap * (1 - 0.352233))), 19.7428),
                             sum(adv40, 19.7428), 6.83313)) ** rank(correlation(rank(vwap), rank(volume), 5.77492)))


def alpha_079(open, close, vwap, adv150, sector, **kwargs):
    """Alpha#79: (rank(delta(IndNeutralize(((close * 0.60733) + (open * (1 - 0.60733))),
IndClass.sector), 1.23438)) < rank(correlation(Ts_Rank(vwap, 3.60973), Ts_Rank(adv150,
9.18637), 14.6644)))"""
    return LessThan(rank(delta(IndNeutralize(((close * 0.60733) + (open * (1 - 0.60733))),
                                             group=sector), 1.23438)),
                    rank(correlation(Ts_Rank(vwap, 3.60973), Ts_Rank(adv150,
                                                                     9.18637),
                                     14.6644)))


def alpha_080(open, high, adv10, industry, **kwargs):
    """Alpha#80: ((rank(Sign(delta(IndNeutralize(((open * 0.868128) + (high * (1 - 0.868128))),
IndClass.industry), 4.04545)))^Ts_Rank(correlation(high, adv10, 5.11456), 5.53756)) * -1)"""
    return ((rank(Sign(delta(IndNeutralize(((open * 0.868128) + (high * (1 - 0.868128))),
                                           group=industry), 4.04545))) ** Ts_Rank(correlation(high, adv10, 5.11456),
                                                                                  5.53756)) * -1)


def alpha_081(volume, vwap, adv10, **kwargs):
    """Alpha#81: ((rank(Log(product(rank((rank(correlation(vwap, sum(adv10, 49.6054),
8.47743))^4)), 14.9655))) < rank(correlation(rank(vwap), rank(volume), 5.07914))) * -1)"""
    return (LessThan(rank(Log(product(rank((rank(correlation(vwap, sum(adv10, 49.6054),
                                                             8.47743)) ** 4)), 14.9655))), rank(
        correlation(rank(vwap), rank(volume), 5.07914))) * -1)


def alpha_082(open, volume, sector, **kwargs):
    """Alpha#82: (min(rank(decay_linear(delta(open, 1.46063), 14.8717)),
Ts_Rank(decay_linear(correlation(IndNeutralize(volume, IndClass.sector), ((open * 0.634196) +
(open * (1 - 0.634196))), 17.4842), 6.92131), 13.4283)) * -1)"""
    return (min(rank(decay_linear(delta(open, 1.46063), 14.8717)),
                Ts_Rank(decay_linear(correlation(IndNeutralize(volume, group=sector), ((open * 0.634196) +
                                                                                       (open * (1 - 0.634196))),
                                                 17.4842), 6.92131), 13.4283)) * -1)


def alpha_083(high, low, close, volume, vwap, **kwargs):
    """Alpha#83: ((rank(delay(((high - low) / (sum(close, 5) / 5)), 2)) * rank(rank(volume))) / (((high -
low) / (sum(close, 5) / 5)) / (vwap - close)))"""
    return ((rank(delay(((high - low) / (sum(close, 5) / 5)), 2)) * rank(rank(volume))) / (((high -
                                                                                             low) / (sum(close,
                                                                                                         5) / 5)) / (
                                                                                                   vwap - close)))


def alpha_084(close, vwap, **kwargs):
    """Alpha#84: SignedPower(Ts_Rank((vwap - ts_max(vwap, 15.3217)), 20.7127), delta(close,
4.96796))"""
    return SignedPower(Ts_Rank((vwap - ts_max(vwap, 15.3217)), 20.7127), delta(close,
                                                                               4.96796))


def alpha_085(high, low, close, volume, adv30, **kwargs):
    """Alpha#85: (rank(correlation(((high * 0.876703) + (close * (1 - 0.876703))), adv30,
9.61331))^rank(correlation(Ts_Rank(((high + low) / 2), 3.70596), Ts_Rank(volume, 10.1595),
7.11408)))"""
    return (rank(correlation(((high * 0.876703) + (close * (1 - 0.876703))), adv30,
                             9.61331)) ** rank(
        correlation(Ts_Rank(((high + low) / 2), 3.70596), Ts_Rank(volume, 10.1595),
                    7.11408)))


def alpha_086(open, close, vwap, adv20, **kwargs):
    """Alpha#86: ((Ts_Rank(correlation(close, sum(adv20, 14.7444), 6.00049), 20.4195) < rank(((open
+ close) - (vwap + open)))) * -1)"""
    return (LessThan(Ts_Rank(correlation(close, sum(adv20, 14.7444), 6.00049), 20.4195), rank(((open
                                                                                                + close) - (
                                                                                                       vwap + open)))) * -1)


def alpha_087(close, vwap, adv81, industry, **kwargs):
    """Alpha#87: (max(rank(decay_linear(delta(((close * 0.369701) + (vwap * (1 - 0.369701))),
1.91233), 2.65461)), Ts_Rank(decay_linear(abs(correlation(IndNeutralize(adv81,
IndClass.industry), close, 13.4132)), 4.89768), 14.4535)) * -1)"""
    return (max(rank(decay_linear(delta(((close * 0.369701) + (vwap * (1 - 0.369701))),
                                        1.91233), 2.65461)), Ts_Rank(decay_linear(abs(correlation(IndNeutralize(adv81,
                                                                                                                group=industry),
                                                                                                  close, 13.4132)),
                                                                                  4.89768), 14.4535)) * -1)


def alpha_088(open, high, low, close, adv60, **kwargs):
    """Alpha#88: min(rank(decay_linear(((rank(open) + rank(low)) - (rank(high) + rank(close))),
8.06882)), Ts_Rank(decay_linear(correlation(Ts_Rank(close, 8.44728), Ts_Rank(adv60,
20.6966), 8.01266), 6.65053), 2.61957))"""
    return min(rank(decay_linear(((rank(open) + rank(low)) - (rank(high) + rank(close))),
                                 8.06882)), Ts_Rank(decay_linear(correlation(Ts_Rank(close, 8.44728), Ts_Rank(adv60,
                                                                                                              20.6966),
                                                                             8.01266), 6.65053), 2.61957))


def alpha_089(low, vwap, adv10, industry, **kwargs):
    """Alpha#89: (Ts_Rank(decay_linear(correlation(((low * 0.967285) + (low * (1 - 0.967285))), adv10,
6.94279), 5.51607), 3.79744) - Ts_Rank(decay_linear(delta(IndNeutralize(vwap,
IndClass.industry), 3.48158), 10.1466), 15.3012))"""
    return (Ts_Rank(decay_linear(correlation(((low * 0.967285) + (low * (1 - 0.967285))), adv10,
                                             6.94279), 5.51607), 3.79744) - Ts_Rank(
        decay_linear(delta(IndNeutralize(vwap,
                                         group=industry), 3.48158), 10.1466), 15.3012))


def alpha_090(low, close, adv40, subindustry, **kwargs):
    """Alpha#90: ((rank((close - ts_max(close, 4.66719)))^Ts_Rank(correlation(IndNeutralize(adv40,
IndClass.subindustry), low, 5.38375), 3.21856)) * -1)"""
    return ((rank((close - ts_max(close, 4.66719))) ** Ts_Rank(correlation(IndNeutralize(adv40,
                                                                                         group=subindustry), low,
                                                                           5.38375), 3.21856)) * -1)


def alpha_091(close, volume, vwap, adv30, industry, **kwargs):
    """Alpha#91: ((Ts_Rank(decay_linear(decay_linear(correlation(IndNeutralize(close,
IndClass.industry), volume, 9.74928), 16.398), 3.83219), 4.8667) -
rank(decay_linear(correlation(vwap, adv30, 4.01303), 2.6809))) * -1)"""
    return ((Ts_Rank(decay_linear(decay_linear(correlation(IndNeutralize(close,
                                                                         group=industry), volume, 9.74928), 16.398),
                                  3.83219), 4.8667) -
             rank(decay_linear(correlation(vwap, adv30, 4.01303), 2.6809))) * -1)


def alpha_092(open, high, low, close, adv30, **kwargs):
    """Alpha#92: min(Ts_Rank(decay_linear(((((high + low) / 2) + close) < (low + open)), 14.7221),
18.8683), Ts_Rank(decay_linear(correlation(rank(low), rank(adv30), 7.58555), 6.94024),
6.80584))"""
    return min(Ts_Rank(decay_linear(((((high + low) / 2) + close) < (low + open)) * 1., 14.7221),
                       18.8683), Ts_Rank(decay_linear(correlation(rank(low), rank(adv30), 7.58555), 6.94024),
                                         6.80584))


def alpha_093(close, vwap, adv81, industry, **kwargs):
    """Alpha#93: (Ts_Rank(decay_linear(correlation(IndNeutralize(vwap, IndClass.industry), adv81,
17.4193), 19.848), 7.54455) / rank(decay_linear(delta(((close * 0.524434) + (vwap * (1 -
0.524434))), 2.77377), 16.2664)))"""
    return (Ts_Rank(decay_linear(correlation(IndNeutralize(vwap, group=industry), adv81,
                                             17.4193), 19.848), 7.54455) / rank(
        decay_linear(delta(((close * 0.524434) + (vwap * (1 -
                                                          0.524434))), 2.77377), 16.2664)))


def alpha_094(vwap, adv60, **kwargs):
    """Alpha#94: ((rank((vwap - ts_min(vwap, 11.5783)))^Ts_Rank(correlation(Ts_Rank(vwap,
19.6462), Ts_Rank(adv60, 4.02992), 18.0926), 2.70756)) * -1)"""
    return ((rank((vwap - ts_min(vwap, 11.5783))) ** Ts_Rank(correlation(Ts_Rank(vwap,
                                                                                 19.6462), Ts_Rank(adv60, 4.02992),
                                                                         18.0926), 2.70756)) * -1)


def alpha_095(open, high, low, adv40, **kwargs):
    """Alpha#95: (rank((open - ts_min(open, 12.4105))) < Ts_Rank((rank(correlation(sum(((high + low)
/ 2), 19.1351), sum(adv40, 19.1351), 12.8742))^5), 11.7584))"""
    return LessThan(rank((open - ts_min(open, 12.4105))), Ts_Rank((rank(correlation(sum(((high + low)
                                                                                         / 2), 19.1351),
                                                                                    sum(adv40, 19.1351),
                                                                                    12.8742)) ** 5), 11.7584))


def alpha_096(close, volume, vwap, adv60, **kwargs):
    """Alpha#96: (max(Ts_Rank(decay_linear(correlation(rank(vwap), rank(volume), 3.83878),
4.16783), 8.38151), Ts_Rank(decay_linear(Ts_ArgMax(correlation(Ts_Rank(close, 7.45404),
Ts_Rank(adv60, 4.13242), 3.65459), 12.6556), 14.0365), 13.4143)) * -1)"""
    return (max(Ts_Rank(decay_linear(correlation(rank(vwap), rank(volume), 3.83878),
                                     4.16783), 8.38151),
                Ts_Rank(decay_linear(Ts_ArgMax(correlation(Ts_Rank(close, 7.45404),
                                                           Ts_Rank(adv60, 4.13242), 3.65459), 12.6556), 14.0365),
                        13.4143)) * -1)


def alpha_097(low, vwap, adv60, industry, **kwargs):
    """Alpha#97: ((rank(decay_linear(delta(IndNeutralize(((low * 0.721001) + (vwap * (1 - 0.721001))),
IndClass.industry), 3.3705), 20.4523)) - Ts_Rank(decay_linear(Ts_Rank(correlation(Ts_Rank(low,
7.87871), Ts_Rank(adv60, 17.255), 4.97547), 18.5925), 15.7152), 6.71659)) * -1)"""
    return ((rank(decay_linear(delta(IndNeutralize(((low * 0.721001) + (vwap * (1 - 0.721001))),
                                                   group=industry), 3.3705), 20.4523)) - Ts_Rank(
        decay_linear(Ts_Rank(correlation(Ts_Rank(low,
                                                 7.87871), Ts_Rank(adv60, 17.255), 4.97547), 18.5925), 15.7152),
        6.71659)) * -1)


def alpha_098(open, vwap, adv5, adv15, **kwargs):
    """Alpha#98: (rank(decay_linear(correlation(vwap, sum(adv5, 26.4719), 4.58418), 7.18088)) -
rank(decay_linear(Ts_Rank(Ts_ArgMin(correlation(rank(open), rank(adv15), 20.8187), 8.62571),
6.95668), 8.07206)))"""
    return (rank(decay_linear(correlation(vwap, sum(adv5, 26.4719), 4.58418), 7.18088)) -
            rank(decay_linear(Ts_Rank(Ts_ArgMin(correlation(rank(open), rank(adv15), 20.8187), 8.62571),
                                      6.95668), 8.07206)))


def alpha_099(high, low, volume, adv60, **kwargs):
    """Alpha#99: ((rank(correlation(sum(((high + low) / 2), 19.8975), sum(adv60, 19.8975), 8.8136)) <
rank(correlation(low, volume, 6.28259))) * -1)"""
    return (LessThan(rank(correlation(sum(((high + low) / 2), 19.8975), sum(adv60, 19.8975), 8.8136)),
                     rank(correlation(low, volume, 6.28259))) * -1)


def alpha_100(high, low, close, volume, adv20, subindustry, **kwargs):
    """Alpha#100: (0 - (1 * (((1.5 * scale(indneutralize(indneutralize(rank(((((close - low) - (high -
close)) / (high - low)) * volume)), IndClass.subindustry), IndClass.subindustry))) -
scale(indneutralize((correlation(close, rank(adv20), 5) - rank(ts_argmin(close, 30))),
IndClass.subindustry))) * (volume / adv20))))"""
    return (0 - (1 * (((1.5 * scale(indneutralize(indneutralize(rank(((((close - low) - (high -
                                                                                         close)) / (
                                                                               high - low)) * volume)),
                                                                group=subindustry), group=subindustry), 1)) -
                       scale(indneutralize((correlation(close, rank(adv20), 5) - rank(ts_argmin(close, 30))),
                                           group=subindustry), 1)) * (volume / adv20))))


def alpha_101(open, high, low, close, **kwargs):
    """Alpha#101: ((close - open) / ((high - low) + .001))"""
    return ((close - open) / ((high - low) + .001))
