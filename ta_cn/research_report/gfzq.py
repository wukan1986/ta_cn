"""
广发证券，研报复现

有关TD系列的指标，由于没有看懂，所以先放着
只测试了一下一维数据，等完全正确了再改成二维版并加快速
对TD有见解的朋友可以与我联系一起完善此部分

"""
import numba
import numpy as np

from ta_cn.wq.arithmetic import sign
from ta_cn.wq.time_series import ts_delta


@numba.jit(nopython=True, cache=True, nogil=True)
def LLT(p, a):
    """LLT低延迟趋势线(Low-lag Trendline), 《短线择时策略研究之三：低延迟趋势线与交易性择时》

    """
    # a = 2/(d+1)
    # 系数
    b1 = a - (a ** 2) / 4
    b2 = (a ** 2) / 2
    b3 = a - 3 * (a ** 2) / 4
    b4 = 2 * (1 - a)
    b5 = (1 - a) ** 2

    llt = p.copy()
    for t in range(2, len(p)):
        c1 = b1 * p[t] + b2 * p[t - 1] - b3 * p[t - 2] + b4 * llt[t - 1] - b5 * llt[t - 2]
        # 处理数据前段为空值的情况，中段出现空值将出错重新计算
        llt[t] = np.where(llt[t - 2] == llt[t - 2], c1, p[t])
    return llt


def TD9(close, n1=4, n2=9):
    """神奇九转。 单边行情下无效

    返回持仓状态，不是买卖信息
    """
    # 前4天
    ud = sign(ts_delta(close, n1))
    setup = ud.copy()

    # 九转
    for i in range(n1, len(close)):
        # 相同就累加昨天的值，不同就设成1或-1,0
        setup[i] = np.where(ud[i] == ud[i - 1], setup[i - 1], 0) + ud[i]

    # 反转信号。-9表示要开始买入，9表示要开始卖出
    signal = np.zeros_like(setup)

    if True:
        # 返回持仓状态
        signal[setup >= n2] = -1
        signal[setup <= -n2] = 1
    else:
        # 返回买卖动作
        signal[setup == n2] = -1
        signal[setup == -n2] = 1

    return signal


def tom_demark_sequential(high, low, close, n1=4, n2=9, n3=13):
    # TODO： 等这里完全正确后再改成二维版
    # 前4天
    ud = sign(ts_delta(close, n1))
    setup = ud.copy()

    # 九转
    for i in range(n1, len(close)):
        # 相同就累加昨天的值，不同就设成1或-1,0
        setup[i] = np.where(ud[i] == ud[i - 1], setup[i - 1], 0) + ud[i]

    # 启动后做多计数条件
    buy_cond = close < ts_delta(low, 2)
    # 启动后做空计数条件
    sell_cond = close > ts_delta(high, 2)

    buy_count = buy_cond * 0
    sell_count = sell_cond * 0

    # 计数 TODO: 这里逻辑可能有问题
    for i in range(n1 + n2 - 1, len(close)):
        if setup[i] <= -n2:
            buy_count[i] = buy_count[i - 1] + buy_cond[i]
        elif setup[i] >= n2:
            sell_count[i] = sell_count[i - 1] + sell_cond[i]

    signal = np.zeros_like(close)
    signal[buy_count >= n3] = 1
    signal[sell_count >= n3] = -1
    return signal


def TD(high, low, close, n1, n2, n3):
    """

    Parameters
    ----------
    n1:
        价格比较滞后期数
    n2:
        价格关系单向连续个数
    n3:
        计数阶段最终信号发出所需计数值

    Returns
    -------

    """
    ud = sign(ts_delta(close, n1))
    ud_acc = ud.copy()
    buy_cnt = np.zeros_like(ud)
    sell_cnt = np.zeros_like(ud)
    for i in range(n1, len(close)):
        # 相同就累加昨天的值
        ud_acc[i] = np.where(ud[i] == ud[i - 1], ud_acc[i - 1], 0) + ud[i]

        if ud_acc[i] == -n2:
            # 昨天买入已经启动了
            a = close[i] >= high[i - 2]
            b = high[i] > high[i - 1]
            c = close[i] > close[i - 1]
            if a & b & c:
                pass
        if ud_acc[i] == n2:
            # 昨天卖出已经启动了
            a = close[i] <= low[i - 2]
            b = low[i] < low[i - 1]
            c = close[i] < close[i - 1]
            if a & b & c:
                pass

    print(ud)
    print(ud_acc)
    # return ud_acc


x = np.array([0, 1, 2, 3, 4,
              5, 6, 7, 8, 9,
              10, 11, 12, 13, 14,
              15, 16, 17, 18, 19,
              5], dtype=float)
tom_demark_sequential(x, 4, 9)
# http://www.snailtoday.com/archives/5469
# https://github.com/dachuanwud/coincock/blob/main/program/%E6%8B%A9%E6%97%B6%E7%AD%96%E7%95%A5_%E5%9B%9E%E6%B5%8B/Signals.py
# https://github.com/Rebeccawing/Quantitative-Contest/blob/master/GFTD.py
# https://github.com/dachuanwud/coincock/blob/main/program/%E6%8B%A9%E6%97%B6%E7%AD%96%E7%95%A5_%E5%9B%9E%E6%B5%8B/Signals.py
# https://github.com/tongtong263/quant_class/blob/75dbfcbca0924a6f829bb9069a7a60bced379213/%E9%87%8F%E5%8C%96%E9%AB%98%E9%98%B6%E6%95%99%E7%A8%8B/xbx_stock_2019/program/%E6%8B%A9%E6%97%B6%E7%AD%96%E7%95%A5_%E5%9B%9E%E6%B5%8B/Signals.py
