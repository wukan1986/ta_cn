"""
通达信公式转alpha101

101 Formulaic Alphas
文档质量一般
1. 部分函数即有全小写，又有大小写混合
2. 很多参数应当是整数，但输入是小数，不得不做修正
"""
from ta_cn.imports import long as L
from ta_cn.utils import round_a_i, round_a_a_i

correlation = round_a_a_i(L.CORREL)
decay_linear = round_a_i(L.WMA)

LessThan = L.LessThan
rank = L.RANK
ts_rank = round_a_i(L.TS_RANK)
scale = L.scale
SignedPower = L.signedpower

IF = L.IF
abs = L.ABS
log = L.LN  # 这里是用的自然对数
MAX = L.MAX2
MIN = L.MIN2
sign = L.SGN

delta = round_a_i(L.DIFF)
ts_max = round_a_i(L.HHV)
ts_argmax = round_a_i(L.HHVBARS)
ts_min = round_a_i(L.LLV)
ts_argmin = round_a_i(L.LLVBARS)
product = round_a_i(L.PRODUCT)
delay = round_a_i(L.REF)
sum = round_a_i(L.SUM)

covariance = round_a_a_i(L.COVAR)
stddev = round_a_i(L.STDP)  # 引入的是全体标准差

indneutralize = L.indneutralize


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
