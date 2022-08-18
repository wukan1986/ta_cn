import pandas as pd
from pandas.testing import assert_frame_equal
from pandas.testing import assert_series_equal

import ta_cn.alphas.test101 as a
import ta_cn.alphas.alpha101 as b

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

    df = {
        'open': open_,
        'high': high,
        'low': low,
        'close': close,
        'returns': returns,
        'volume': volume,
        'vwap': vwap,
        'adv5': adv20,
        'adv10': adv20,
        'adv15': adv20,
        'adv20': adv20,
        'adv30': adv20,
        'adv40': adv20,
        'adv50': adv20,
        'adv60': adv20,
        'adv81': adv20,
        'adv120': adv20,
        'adv150': adv20,
        'adv180': adv20,
        'subindustry': group,
        'sector': group,
        'industry': group,
        'cap': cap,
    }

    # kwargs_w = {k: WArr.from_array(v, direction='down') for k, v in df.items()}

    kwargs_l = {k: v.stack() for k, v in df.items()}
    kwargs_l = pd.DataFrame(kwargs_l)
    kwargs_l.index.names = ['date', 'asset']
    kwargs_l = kwargs_l.to_dict(orient='series')

    for i in range(1, 100 + 1):
        # if i not in (62,):
        #     continue
        name = f'alpha_{i:03d}'
        f1 = getattr(a, name, None)
        f2 = getattr(b, name, None)
        if f1 is None:
            continue
        print(name)
        r1 = f1(**kwargs_l)
        r2 = f2(**kwargs_l)
        assert_series_equal(r1, r2)
