"""
以下是在长表上的动态复权和动态参数的示例
"""
import numpy as np
import pandas as pd

import talib as ta

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

# 周期等参数需要两行之间比较不同，然后不同周期再合并考虑

df = {
    'open': pd.DataFrame(o).stack(),
    'high': pd.DataFrame(h).stack(),
    'low': pd.DataFrame(l).stack(),
    'close': pd.DataFrame(c).stack(),
    'p1': pd.DataFrame(p1).stack(),
    'p2': pd.DataFrame(p2).stack(),
    'factor': pd.DataFrame(f).stack(),
    'up': pd.DataFrame(up).stack(),
    'down': pd.DataFrame(down).stack(),
}
df = pd.DataFrame(df)
df.index.names = ['date', 'asset']

date = df.index.levels[0]


def func(df):
    """分块计算指标"""

    def f0(x):
        return x['factor'] / x['factor'].iloc[-1]

    def f1(x):
        return ta.SMA(x['close'] * x['f'], timeperiod=x['p1'].iloc[-1])

    def f2(x):
        return ta.ATR(x['high'] * x['f'], x['low'] * x['f'], x['close'] * x['f'], timeperiod=x['p2'].iloc[-1])

    df['f'] = df.groupby(by='asset', group_keys=False).apply(f0)
    ma = df.groupby(by='asset', group_keys=False).apply(f1)
    atr = df.groupby(by='asset', group_keys=False).apply(f2)

    # 这里的改动并不影响结果
    df['up'] = (ma + atr)
    df['down'] = (ma - atr)
    return df[['up', 'down']]


def loop(func,
         df,
         date,
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

    def same_slice(df, slicer, date0, date1):
        p0 = df.loc[date0, slicer]
        p1 = df.loc[date1, slicer]
        return np.allclose(p0, p1)

    def max_period(df, periods, date0):
        p = df.loc[date0, periods]
        return max(p.max())

    # 将日期准备
    end = 0
    for i, d in enumerate(date):
        if is_backtest and i < len(date) - 1:
            if same_slice(df, slicer, date[i], date[i + 1]):
                continue

        start = end

        pre_start = int(max_period(df, periods, date[i])) + pre_load
        pre_start = max(start - pre_start, 0)
        end = i + 1

        print(f'当前:{i}, 更新:[{start},{end}), 加载:[{pre_start},{end}), 步长:{end - start}')
        pre_start_date = date[pre_start]
        end_date = date[end - 1]  # 时间切片时是左闭右闭

        # 切片
        # 迭代计算, 可能会有累积计算结果的需求
        func_outputs = func(df.loc[pre_start_date:end_date, input_args + periods + output_args])
        df.loc[pre_start_date:end_date, output_args] = func_outputs


loop(func,
     df,
     date,
     ['open', 'high', 'low', 'close', 'factor'],
     ['p1', 'p2', 'factor'],
     ['p1', 'p2'],
     ['up', 'down'],
     is_backtest=True)

# up与down是我们想要的结果
print(df[['up', 'down']])
