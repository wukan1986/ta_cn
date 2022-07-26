import pandas as pd

import ta_cn.talib as ta
from ta_cn.alpha import RANK
from ta_cn.preprocess import demean
from ta_cn.utils import dataframe_groupby_apply, series_groupby_apply

ta.init(mode=1, skipna=False)

pd._testing._N = 500
pd._testing._K = 30

open_ = pd._testing.makeTimeDataFrame() + 5
high = pd._testing.makeTimeDataFrame() + 10
low = pd._testing.makeTimeDataFrame() + 5
close = pd._testing.makeTimeDataFrame() + 5
group = close.copy() * 100 // 1 % 5

df = {
    'open_': open_.stack(),
    'high': high.stack(),
    'low': low.stack(),
    'close': close.stack(),
    'group': group.stack(),
}
df = pd.DataFrame(df)
df.index.names = ['date', 'asset']
kwargs = df.to_dict(orient='series')

# 套上装饰器，实现组内计算
SMA = series_groupby_apply(ta.SMA, by='asset', dropna=True)
ATR = dataframe_groupby_apply(ta.ATR, by='asset', dropna=True)
# 横截面
RANK = series_groupby_apply(RANK, by='date', dropna=True)
# 行业中性化
indneutralize = dataframe_groupby_apply(demean, by=['date', 'group'], dropna=False)

# 单输入
r = SMA(df['close'], timeperiod=10)
print(r.unstack())
# 多输入
r = ATR(df['high'], df['low'], df['close'], 10)
print(r.unstack())
# 横截面
r = RANK(df['close'])
print(r.unstack())
r = indneutralize(df['close'], group=df['group'])

print(r.unstack())
