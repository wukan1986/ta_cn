import pandas as pd

from ta_cn.imports.gtja_long import RANK
from ta_cn.imports.long import SMA_TA, ATR, group_neutralize

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

# 单输入
r = SMA_TA(df['close'], timeperiod=10)
print(r.unstack())
# 多输入
r = ATR(df['high'], df['low'], df['close'], 10)
print(r.unstack())
# 横截面
r = RANK(df['close'])
print(r.unstack())
r = group_neutralize(df['close'], df['group'])

print(r.unstack())
