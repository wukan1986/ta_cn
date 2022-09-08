"""
通达信公式转alpha101

101 Formulaic Alphas
文档质量一般
1. 部分函数即有全小写，又有大小写混合
2. 很多参数应当是整数，但输入是小数，不得不做修正
"""

from ..imports import wide as W
from ..utils import round_a_i, round_a_a_i

correlation = round_a_a_i(W.CORREL)
decay_linear = round_a_i(W.WMA)

LessThan = W.LessThan
rank = W.RANK
ts_rank = round_a_i(W.TS_RANK)
scale = W.scale
SignedPower = W.signed_power

IF = W.if_else
abs = W.abs
log = W.log  # 这里是用的自然对数
MAX = W.MAX2
MIN = W.MIN2
sign = W.sign

delta = round_a_i(W.ts_delta)
ts_max = round_a_i(W.ts_max)
ts_argmax = round_a_i(W.ts_arg_max)
ts_min = round_a_i(W.ts_min)
ts_argmin = round_a_i(W.ts_arg_min)
product = round_a_i(W.ts_product)
delay = round_a_i(W.ts_delay)
sum = round_a_i(W.ts_sum)

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
