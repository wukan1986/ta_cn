import pandas as pd
from pandas._testing import assert_series_equal

import ta_cn.alpha191_w as a
from ta_cn.utils_wide import WRes

if __name__ == '__main__':
    pd._testing._N = 500
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

    kwargs = {
        'OPEN': open_,
        'HIGH': high,
        'LOW': low,
        'CLOSE': close,
        'RET': returns,
        'VOLUME': volume,
        'AMOUNT': volume * 100,
        'VWAP': vwap,
        'DTM': high,
        'DBM': low,
        'MKT': high,
        'SMB': low,
        'HML': close,
        'BANCHMARKINDEXOPEN': high,
        'BANCHMARKINDEXCLOSE': low,
    }

    kwargs = {k: WRes.from_array(v, direction='down') for k, v in kwargs.items()}

    for i in range(1, 191 + 1):
        # 165 183 是MAX 与 SUMAC 问题
        # 36
        if i in (165, 183, 30):
            continue
        name = f'alpha_{i:03d}'
        f1 = getattr(a, name, None)

        if f1 is None:
            continue
        print(name)
        r1 = f1(**kwargs)
        #print(r1.raw())
