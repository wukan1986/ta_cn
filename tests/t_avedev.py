import time

import numpy as np

from ta_cn import np_to_pd


def AVEDEV0(real, timeperiod: int = 100):
    return np_to_pd(real).rolling(window=timeperiod).apply(lambda x: (np.abs(x - x.mean())).mean(), raw=True)


def AVEDEV1(real, timeperiod: int = 100):
    """平均绝对偏差"""

    def mad(x):
        return np.abs(x - x.mean()).mean()

    return np_to_pd(real).rolling(window=timeperiod).apply(mad, raw=True)


def AVEDEV2(real, timeperiod: int = 100):
    """搞了新算法，怎么速度没有rolling快？"""

    def mad(x):
        return np.abs(x - x.mean()).mean()

    arr = np.lib.stride_tricks.sliding_window_view(real, timeperiod, axis=0)
    out = np.full_like(real, fill_value=np.nan)
    # apply_along_axis居然比rolling慢
    out[timeperiod - 1:] = np.apply_along_axis(mad, axis=real.ndim, arr=arr)

    return out


a = np.random.rand(10000).reshape(-1, 2)

if __name__ == '__main__':
    funcs = ['AVEDEV']
    for func in funcs:
        print(func)

        t1 = time.time()
        r1 = AVEDEV1(a).iloc[:, 0]
        t2 = time.time()
        r2 = AVEDEV2(a)[:, 0]
        t3 = time.time()

        print(t2 - t1, t3 - t2)

        # pd.DataFrame({'TA': r1, 'MY': r2}).plot()
        # pd.DataFrame({'MY': r2, 'TA': r1}).plot()
        # plt.show()
