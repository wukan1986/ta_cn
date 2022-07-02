import pandas as pd

import ta_cn.alpha191 as a191

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
        'BANCHMARKINDEXOPEN': high.stack(),
        'BANCHMARKINDEXCLOSE': low.stack(),
    }
    df = pd.DataFrame(df)
    df.index.names = ['date', 'asset']
    kwargs = df.to_dict(orient='series')

    for i in range(1, 191 + 1):
        # if i not in (62,):
        #     continue
        name = f'alpha_{i:03d}'
        f = getattr(a191, name, None)
        if f is None:
            continue
        print(name)
        r = f(**kwargs)
        print(r.unstack())
