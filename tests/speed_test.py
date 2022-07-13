import time

import bottleneck as bn
import pandas as pd
import polars as pl
import talib
from pandas._testing import assert_series_equal

import ta_cn.talib as ta2d

ta2d.init(mode=1, skipna=False)

pl.Config.set_tbl_rows(50)


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
    pd._testing._N = 1000
    pd._testing._K = 30

    open_ = pd._testing.makeTimeDataFrame() + 5
    high = pd._testing.makeTimeDataFrame() + 10
    low = pd._testing.makeTimeDataFrame() + 5
    close = pd._testing.makeTimeDataFrame() + 5
    volume = pd._testing.makeTimeDataFrame() * 10 + 100
    vwap = pd._testing.makeTimeDataFrame()
    adv20 = pd._testing.makeTimeDataFrame()
    returns = pd._testing.makeTimeDataFrame()
    cap = pd._testing.makeTimeDataFrame() * 100 + 100
    group = close.copy() * 100 // 1 % 5

    df = {
        'OPEN': open_.stack(),
        'HIGH': high.stack(),
        'LOW': low.stack(),
        'CLOSE': close.stack(),
        'RET': returns.stack(),
        'VOLUME': volume.stack(),
        'AMOUNT': volume.stack() * 100,
        'VWAP': vwap.stack(),
        'DTM': high.stack(),
        'DBM': low.stack(),
        'MKT': high.stack(),
        'SMB': low.stack(),
        'HML': close.stack(),
        'BANCHMARKINDEXOPEN': high.stack(),
        'BANCHMARKINDEXCLOSE': low.stack(),
    }
    df = pd.DataFrame(df)
    df.index.names = ['date', 'asset']
    df1 = pl.from_pandas(df.reset_index())

    for f in [f1, f2, f3, f4, f5, f6]:
        t0 = time.time()
        f(df, df1)
        t1 = time.time()
        print(f.__name__, t1 - t0)

# f1 0.060014963150024414
# f2 0.07854080200195312
# f3 0.05702543258666992
# f4 0.06399655342102051
# f5 0.07001638412475586
# f6 0.25406837463378906

# f1 0.007016181945800781
# f2 0.00998830795288086
# f3 0.012003898620605469
# f4 0.015001296997070312
# f5 0.015004396438598633
# f6 0.04201769828796387
