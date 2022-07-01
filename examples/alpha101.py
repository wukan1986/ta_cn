import pandas as pd

import ta_cn.alpha101 as a101

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
        'open_': open_.stack(),
        'high': high.stack(),
        'low': low.stack(),
        'close': close.stack(),
        'returns': returns.stack(),
        'volume': volume.stack(),
        'vwap': vwap.stack(),
        'adv5': adv20.stack(),
        'adv10': adv20.stack(),
        'adv15': adv20.stack(),
        'adv20': adv20.stack(),
        'adv30': adv20.stack(),
        'adv40': adv20.stack(),
        'adv50': adv20.stack(),
        'adv60': adv20.stack(),
        'adv81': adv20.stack(),
        'adv120': adv20.stack(),
        'adv150': adv20.stack(),
        'adv180': adv20.stack(),
        'subindustry': group.stack(),
        'sector': group.stack(),
        'industry': group.stack(),
        'cap': cap.stack(),
    }
    df = pd.DataFrame(df)
    df.index.names = ['date', 'asset']
    kwargs = df.to_dict(orient='series')

    # for i in range(1, 19):
    for i in range(80, 101 + 1):
        if i in (84,):
            continue
        name = f'alpha_{i:03d}'
        f = getattr(a101, name, None)
        if f is None:
            continue
        print(name)
        r = f(**kwargs)
        print(r.unstack())
