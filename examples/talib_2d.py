import numpy as np

# 原版talib,不支持二维数据
# import talib as ta

# 新版talib,只要替换引用即可直接支持二维数据
import ta_cn.talib as ta
from ta_cn.utils import pushna, pullna

if __name__ == '__main__':
    # 准备数据
    h = np.random.rand(10000000).reshape(-1, 50000) + 10
    l = np.random.rand(10000000).reshape(-1, 50000)
    c = np.random.rand(10000000).reshape(-1, 50000)

    # 几个调用函数演示
    r = ta.ATR(h, l, c, 10)
    print(r)
    x, y, z = ta.BBANDS(c, timeperiod=10, nbdevup=2, nbdevdn=2)
    print(z)

    # 将少量值设置为空，用来模拟停牌
    c[c < 0.05] = np.nan

    # 跳过停牌进行计算，再还原的演示
    arr, row, col = pushna(c, direction='down')
    rr = ta.SMA(real=arr, timeperiod=10)
    r = pullna(rr, row, col)
    print(r)
