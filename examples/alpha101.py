import os
import sys

import pandas as pd
from numpy.testing import assert_allclose
from pandas._testing import assert_series_equal, assert_numpy_array_equal

from ta_cn.utils_wide import WArr

os.environ['TA_CN_MODE'] = 'WIDE'
import ta_cn.alphas.alpha101 as w

# 移除，这样就可以重复导入包了
sys.modules.pop('ta_cn.alphas.alpha101')

os.environ['TA_CN_MODE'] = 'LONG'
import ta_cn.alphas.alpha101 as l
import ta_cn.alphas.test101 as t

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

    kwargs_w = {k: WArr.from_array(v, direction='down') for k, v in df.items()}

    kwargs_l = {k: v.stack() for k, v in df.items()}
    kwargs_l = pd.DataFrame(kwargs_l)
    kwargs_l.index.names = ['date', 'asset']
    kwargs_l = kwargs_l.to_dict(orient='series')

    for i in range(1, 101 + 1):
        # if i in (-100,):
        #     continue
        name = f'alpha_{i:03d}'
        ft = getattr(t, name, None)
        fl = getattr(l, name, None)
        fw = getattr(w, name, None)

        print(name)
        rt = ft(**kwargs_l)
        rl = fl(**kwargs_l)
        rw = fw(**kwargs_w)
        # 比较 原版公式 与 优化后公式的 结果是否相同
        assert_series_equal(rt, rl)
        # 比较 长表 与 宽表 结果是否相同
        if i == 100:
            # alpha 100 scale后有少量误差，只能用allclose
            # scale(indneutralize(t1, group=subindustry), 1.)
            assert_allclose(rw.raw(), rl.unstack().values)
        else:
            assert_numpy_array_equal(rw.raw(), rl.unstack().values)
