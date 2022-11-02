import numpy as np

from ta_cn.chip import chip, WINNER, COST

high = np.array([10.4, 10.2, 10.2, 10.4, 10.5, 10.7, 10.7, 10.7, 10.8, 10.9])
low = np.array([10.3, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 10.9])
turnover = np.array([0.3, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])

out, grid = chip(high, high, low, low, turnover, step=0.1)
y = WINNER(out, grid, 10.5)
print(y)
y = COST(out, grid, 0.5)
print(y)
