import time

import bottleneck as bn
import numpy as np
import pandas as pd
import polars as pl
import talib

import ta_cn.talib as ta2d

ta2d.init(mode=1, skipna=False)

pl.Config.set_tbl_rows(50)

print(pl.__version__)


def f1(df, ldf):
    # 最快，因为同资产一起处理的，调用底层库次数少
    return df.groupby(by='asset').apply(lambda x: bn.move_mean(x, 5, axis=0))


def f2(df, ldf):
    # 看来Rust语言底层做得不错
    a = ldf.select([
        'date', 'asset',
        pl.all().exclude(['date', 'asset']).rolling_mean(5).over('asset').suffix('_sma')
    ])
    return a


def f3(df, ldf):
    # 自己的迭代封装看来也可以，只比Rust的差一点点
    return df.groupby(by='asset').apply(lambda x: ta2d.SMA(x, timeperiod=5))


def f4(df, ldf):
    # 比自己的封装版要差一点点
    a = ldf.select([
        'date', 'asset',
        pl.all().exclude(['date', 'asset']).apply(lambda x: pl.Series(bn.move_mean(x, 5))).over('asset').suffix('_sma')
    ])
    return a


def f5(df, ldf):
    # 比自己的封装版要差一点点
    a = ldf.select([
        'date', 'asset',
        pl.all().exclude(['date', 'asset']).apply(lambda x: pl.Series(talib.SMA(x.to_numpy(), 5))).over('asset').suffix(
            '_sma')
    ])
    return a


def f6(df, ldf):
    return df.groupby(by='asset').rolling(5).mean()


if __name__ == '__main__':
    c = np.random.rand(1000000).reshape(-1, 5000)
    c = pd.DataFrame(c).stack()

    df = {i: c for i in range(100)}
    df = pd.DataFrame(df)
    df.index.names = ['date', 'asset']
    df1 = pl.from_pandas(df.reset_index())

    for f in [f1, f2, f3, f4, f5, f6]:
        t0 = time.time()
        f(df, df1)
        t1 = time.time()
        print(f.__name__, t1 - t0)

# f1 1.5436947345733643
# f2 3.0246715545654297
# f3 6.506034851074219
# f4 10.475429773330688
# f5 10.043684959411621
# f6 29.300340175628662
