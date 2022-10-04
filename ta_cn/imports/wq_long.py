"""
公式转alpha101

101 Formulaic Alphas
文档质量一般
1. 部分函数即有全小写，又有大小写混合
2. 很多参数应当是整数，但输入是小数，不得不做修正
"""
from ..imports import long_wq as L_WQ

from ..utils import round_a_i, round_a_a_i

correlation = round_a_a_i(L_WQ.ts_corr)
decay_linear = round_a_i(L_WQ.ts_decay_linear)

LessThan = L_WQ.less
rank = L_WQ.rank
ts_rank = round_a_i(L_WQ.ts_rank)
scale = L_WQ.scale
SignedPower = L_WQ.signed_power

IF = L_WQ.if_else
abs = L_WQ.abs_
log = L_WQ.log  # 这里是用的自然对数
MAX = L_WQ.max_
MIN = L_WQ.min_
sign = L_WQ.sign

delta = round_a_i(L_WQ.ts_delta)
ts_max = round_a_i(L_WQ.ts_max)
ts_argmax = round_a_i(L_WQ.ts_arg_max)
ts_min = round_a_i(L_WQ.ts_min)
ts_argmin = round_a_i(L_WQ.ts_arg_min)
product = round_a_i(L_WQ.ts_product)
delay = round_a_i(L_WQ.ts_delay)
sum = round_a_i(L_WQ.ts_sum)

covariance = round_a_a_i(L_WQ.ts_covariance)
stddev = round_a_i(L_WQ.ts_std_dev)  # 引入的是全体标准差

indneutralize = L_WQ.group_neutralize

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
