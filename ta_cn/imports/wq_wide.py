"""
公式转alpha101

101 Formulaic Alphas
文档质量一般
1. 部分函数即有全小写，又有大小写混合
2. 很多参数应当是整数，但输入是小数，不得不做修正
"""
from ..imports import wide_wq as W_WQ
from ..utils import round_a_i, round_a_a_i

correlation = round_a_a_i(W_WQ.ts_corr)
decay_linear = round_a_i(W_WQ.ts_decay_linear)

LessThan = W_WQ.less
rank = W_WQ.rank
ts_rank = round_a_i(W_WQ.ts_rank)
scale = W_WQ.scale
SignedPower = W_WQ.signed_power

IF = W_WQ.if_else
abs = W_WQ.abs_
log = W_WQ.log  # 这里是用的自然对数
MAX = W_WQ.max_
MIN = W_WQ.min_
sign = W_WQ.sign

delta = round_a_i(W_WQ.ts_delta)
ts_max = round_a_i(W_WQ.ts_max)
ts_argmax = round_a_i(W_WQ.ts_arg_max)
ts_min = round_a_i(W_WQ.ts_min)
ts_argmin = round_a_i(W_WQ.ts_arg_min)
product = round_a_i(W_WQ.ts_product)
delay = round_a_i(W_WQ.ts_delay)
sum = round_a_i(W_WQ.ts_sum)

covariance = round_a_a_i(W_WQ.ts_covariance)
stddev = round_a_i(W_WQ.ts_std_dev)  # 引入的是全体标准差

indneutralize = W_WQ.group_neutralize

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
