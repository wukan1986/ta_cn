"""
通达信公式转alpha101

101 Formulaic Alphas
文档质量一般
1. 部分函数即有全小写，又有大小写混合
2. 很多参数应当是整数，但输入是小数，不得不做修正
"""
from functools import wraps

from ta_cn.imports import wide as W


def round_a_i(func):
    """将参数 向量浮点 调整成 向量整数"""

    @wraps(func)
    def decorated(a, i):
        return func(a, round(i))

    return decorated


def round_a_a_i(func):
    """将参数 向量向量浮点 调整成 向量向量整数"""

    @wraps(func)
    def decorated(a, b, i):
        return func(a, b, round(i))

    return decorated


correlation = round_a_a_i(W.CORREL)
decay_linear = round_a_i(W.WMA)

LessThan = W.LessThan
rank = W.RANK
ts_rank = round_a_i(W.TS_RANK)
scale = W.scale
SignedPower = W.signedpower

IF = W.IF
abs = W.ABS
log = W.LN  # 这里是用的自然对数
MAX = W.MAX2
MIN = W.MIN2
sign = W.SGN

delta = round_a_i(W.DIFF)
ts_max = round_a_i(W.HHV)
ts_argmax = round_a_i(W.HHVBARS)
ts_min = round_a_i(W.LLV)
ts_argmin = round_a_i(W.LLVBARS)
product = round_a_i(W.PRODUCT)
delay = round_a_i(W.REF)
sum = round_a_i(W.SUM)

covariance = round_a_a_i(W.COVAR)
stddev = round_a_i(W.STDP)  # 引入的是全体标准差

indneutralize = W.indneutralize


# 部分别名，这样官方公式可以减少改动
Ts_Rank = ts_rank
IndNeutralize = indneutralize
Ts_ArgMax = ts_argmax
Ts_ArgMin = ts_argmin
LessThan = LessThan
min = MIN
max = MAX
Sign = sign
Log = log
