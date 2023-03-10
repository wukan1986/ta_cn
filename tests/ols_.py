import time

import numpy as np
import statsmodels.api as sm
from statsmodels.regression.rolling import RollingOLS
from ta_cn.regress import multiple_regress, ts_multiple_regress

y = np.random.rand(1000)
y[1] = np.nan
x = np.random.rand(1000 * 4).reshape(-1, 4)
x = np.random.rand(1000 * 1)#.reshape(-1, 4)
# x[1, 1] = np.nan
coef, residual, _ = multiple_regress(y, x, add_constant=False)
t1 = time.time()
coef, residual, _ = multiple_regress(y, x)
t2 = time.time()
# print(residual)

t = sm.add_constant(x)
model = sm.OLS(y, t)
results = model.fit()
t3 = time.time()
# print(y-results.fittedvalues)
print(t2 - t1, t3 - t2)

coef, residual = ts_multiple_regress(y, x, timeperiod=80, add_constant=True)
t1 = time.time()
coef, residual = ts_multiple_regress(y, x, timeperiod=10, add_constant=True)
print(coef)
t2 = time.time()
t = sm.add_constant(x)
model = RollingOLS(y, t, window=10)
results = model.fit()

t3 = time.time()
print(results.params)
print(t2 - t1, t3 - t2)
