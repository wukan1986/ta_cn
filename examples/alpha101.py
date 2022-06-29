import ta_cn.alpha101 as a101

if __name__ == '__main__':
    import pandas as pd

    pd._testing._N = 250
    pd._testing._K = 30

    open_ = pd._testing.makeTimeDataFrame()
    high = pd._testing.makeTimeDataFrame() + 10
    low = pd._testing.makeTimeDataFrame()
    close = pd._testing.makeTimeDataFrame()
    volume = pd._testing.makeTimeDataFrame() * 10 + 100
    vwap = pd._testing.makeTimeDataFrame()
    adv20 = pd._testing.makeTimeDataFrame()
    returns = pd._testing.makeTimeDataFrame()

    df = {
        'open_': open_.stack(),
        'high': high.stack(),
        'low': low.stack(),
        'close': close.stack(),
        'returns': returns.stack(),
        'volume': volume.stack(),
        'vwap': vwap.stack(),
        'adv20': adv20.stack(),
    }
    df = pd.DataFrame(df)
    df.index.names = ['date', 'asset']
    kwargs = df.to_dict(orient='series')

    for i in range(1, 19):
        name = f'alpha_{i:03d}'
        f = getattr(a101, name, None)
        if f is None:
            continue
        print(name)
        r = f(**kwargs)
        print(r.unstack())
