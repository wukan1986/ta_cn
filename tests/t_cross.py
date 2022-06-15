import numpy as np

from ta_cn.logical import CROSS
from ta_cn.nb import _FILTER_2d_nb
from ta_cn.logical import FILTER

a = np.random.rand(10000)
b = np.random.rand(10000)

if __name__ == '__main__':
    a = np.array([[4, 1, 3, 4, 6, 7], [4, 1, 3, 4, 6, 7]]).T
    b = np.array([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]]).T
    c = CROSS(a, b)

    a = np.array([[1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, ], [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, ]]).T
    b = FILTER(a, 5)
    print(a)
    print(b)
