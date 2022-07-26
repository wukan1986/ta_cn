"""
以下是在宽表上的动态复权和动态参数的示例
"""
import numpy as np

import ta_cn.talib as ta

# 默认会启用模式1，这里设置成模式二
# 注意：周期等参数一定得使用命名参数，开高低收等一定要使用位置参数
ta.init(mode=2)

# 准备数据
o = np.random.rand(1000000).reshape(-1, 5000)
h = np.random.rand(1000000).reshape(-1, 5000) + 10
l = np.random.rand(1000000).reshape(-1, 5000)
c = np.random.rand(1000000).reshape(-1, 5000)

# 周期参数
p1 = np.empty_like(c)
p1[:] = 20
p1[:150] = 5
p1[:120] = 10
p1[:50] = 30

p2 = np.empty_like(c)
p2[:] = 10
p2[:180] = 15
p2[:110] = 20
p2[:70] = 10

# 后复权因子
f = np.empty_like(c)
f[:] = 1.5
f[:180] = 1.3
f[:110] = 1.2
f[:60] = 1.1

# 输出
up = np.empty_like(c)
down = np.empty_like(c)


def func(open_, high, low, close, factor,
         period1, period2):
    """分块计算指标"""

    # 后复权转前复权
    f = factor / factor[-1]
    open_ *= f
    high *= f
    low *= f
    close *= f

    # 计算指标
    ma = ta.SMA(close, timeperiod=period1)
    atr = ta.ATR(high, low, close, timeperiod=period2)

    # 每天记录新值
    return (ma + atr), (ma - atr)


def loop(func,
         input_args,
         slicer,
         periods,
         output_args,
         is_backtest=True,
         pre_load=0,
         ):
    """按天进行循环

    Parameters
    ----------
    func:
        计算函数
    input_args: list
        输入矩阵列表
    slicer: list
        切片器
    periods: list
        周期矩阵
    output_args: list
        输出矩阵列表
    is_backtest: bool
        是否回测模式：
        True: 回测。有全部数据，所以可以通过提前加载参数，分块计算，实现加速
        False: 仿真。行情按天推送，只能每天都算
    pre_load: int
         调整值，可以加载更多数据
    """

    def same_slice(ps, i):
        for p in ps:
            if not np.all(p[i] == p[i + 1]):
                return False
        return True

    def max_period(ps, i):
        m = -np.inf
        for p in ps:
            m = max(max(p[i]), m)
        return m

    end = 0
    real = input_args[0]
    for i in range(len(real)):
        # 1. 明天的参数是未知的，而这里为了排除重复计算，提前预取了明天的值
        # 2. 实盘时，每天都是最后一天
        if is_backtest and i < len(real) - 1:
            # 1. 数据最后，没有明天，不得跳过，必须计算一次
            if same_slice(slicer, i):
                # 2. 与明天的参数一样，跳过
                continue

        # 上期的结束就是这期的开始
        start = end
        # 预加载长度，对于EMA可能需要加载的更多，这里要灵活变动
        pre_start = int(max_period(periods, i)) + pre_load
        pre_start = max(start - pre_start, 0)
        end = i + 1

        print(f'当前:{i}, 更新:[{start},{end}), 加载:[{pre_start},{end}), 步长:{end - start}')

        # 切片
        func_args = [v[pre_start:end] for v in input_args]
        func_periods = [v[i] for v in periods]
        # 迭代计算, 可能会有累积计算结果的需求
        func_outputs = func(*func_args, *func_periods)

        # 只取后一段进行更新
        for x, y in zip(output_args, func_outputs):
            x[start:end] = y[start - end:]


loop(func,
     [o, h, l, c, f],
     [p1, p2, f],
     [p1, p2],
     [up, down],
     is_backtest=True)

# up与down是我们想要的结果
print(up)
print(down)
