import pandas as pd
from pandas._testing import assert_series_equal

from ta_cn.imports.long import A_div_AB_1, A_div_AB_2
from ta_cn.imports.wide import MA
from ta_cn.utils import np_to_pd

if __name__ == '__main__':
    pd._testing._N = 500
    pd._testing._K = 30

    close = pd._testing.makeTimeDataFrame()
    group = close.copy() * 500 // 1 % 5

    # 移动平均需要处理一下
    sma20 = MA(close, 20)
    sma20 = np_to_pd(sma20.raw(), index=close.index, columns=close.columns)

    df = {
        'close': close,
        'group': group,
        'c_gt_sma': close > sma20,
    }

    kwargs_l = {k: v.stack() for k, v in df.items()}
    kwargs_l = pd.DataFrame(kwargs_l)
    kwargs_l.index.names = ['date', 'asset']
    kwargs_l = kwargs_l.to_dict(orient='series')

    r = A_div_AB_1(kwargs_l['close'])
    print(r)
    r = A_div_AB_2(kwargs_l['c_gt_sma'], kwargs_l['group'])
    print(r)
