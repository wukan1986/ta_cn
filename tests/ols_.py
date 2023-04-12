import time

import numpy as np
import statsmodels.api as sm
from statsmodels.regression.rolling import RollingOLS

from ta_cn.regress import multiple_regress, ts_multiple_regress

y = np.random.rand(1000)
# y[1] = np.nan
x = np.random.rand(1000 * 4).reshape(-1, 4)
x = np.random.rand(1000 * 1)  # .reshape(-1, 4)
# x[1, 1] = np.nan
residual, y_hat, coef = multiple_regress(y, x, add_constant=False)
t1 = time.time()
residual, y_hat, coef = multiple_regress(y, x, add_constant=True)
t2 = time.time()
print(coef)
print(residual[:10])

t = sm.add_constant(x)
model = sm.OLS(y, t)
results = model.fit()
t3 = time.time()
print(results.params)
print((y-results.fittedvalues)[:10])
print(t2 - t1, t3 - t2)

residual, y_hat, coef = ts_multiple_regress(y, x, timeperiod=80, add_constant=True)
t1 = time.time()
residual, y_hat, coef = ts_multiple_regress(y, x, timeperiod=10, add_constant=True)
print(coef)
t2 = time.time()
t = sm.add_constant(x)
model = RollingOLS(y, t, window=10)
results = model.fit()

t3 = time.time()
print(results.params)
print(t2 - t1, t3 - t2)
