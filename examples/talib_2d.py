import numpy as np

# 新版talib,只要替换引用即可直接支持二维数据
import ta_cn.talib as ta

# 原版talib,不支持二维数据
# import talib as ta


if __name__ == '__main__':
    # 准备数据
    h = np.random.rand(10000000).reshape(-1, 50000) + 10
    l = np.random.rand(10000000).reshape(-1, 50000)
    c = np.random.rand(10000000).reshape(-1, 50000)

    r = ta.SMA(real=c, timeperiod=10)
    print(r)
    r = ta.ATR(h, l, c, 10)
    print(r)
    x, y, z = ta.BBANDS(c, timeperiod=10, nbdevup=2, nbdevdn=2)
    print(z)
