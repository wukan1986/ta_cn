import pandas as pd
from pandas._testing import assert_series_equal

from ta_cn.wq.group import group_percentage, group_neutralize, group_min, group_count, group_scale, group_rank, \
    group_normalize, group_mean

if __name__ == '__main__':
    pd._testing._N = 500
    pd._testing._K = 30

    close = pd._testing.makeTimeDataFrame() + 5
    group = close.copy() * 100 // 1 % 5

    df = {
        'close': close,
        'sector': group,
    }

    kwargs_l = {k: v.stack() for k, v in df.items()}
    kwargs_l = pd.DataFrame(kwargs_l)
    kwargs_l.index.names = ['date', 'asset']
    kwargs_l = kwargs_l.to_dict(orient='series')

    # r = group_percentage(kwargs_l['close'], kwargs_l['sector'], percentage=0.1)
    # print(r)
    # r = group_percentage(kwargs_l['close'], kwargs_l['sector'], percentage=0.9)
    # print(r)
    # r = group_neutralize(kwargs_l['close'], kwargs_l['sector'])
    # print(r)
    # r = group_normalize(kwargs_l['close'], kwargs_l['sector'])
    # print(r)
    r = group_mean(kwargs_l['close'], kwargs_l['close'],kwargs_l['sector'])
    print(r)
