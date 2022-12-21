# 此处引入库要小心，有可能打破只想用talib二维库的需求

# 按股票分组，计算时序指标。注意，组内时序需要已经排序
BY_ASSET = 'asset'
# 按时间分组。计算横截面
BY_DATE = 'date'
# 横截面上进行行业中性化
BY_GROUP = ['date', 'group']

# 浮点数比较精度
# 实测遇到了1.6518123e-06这种实际为0的情况
# 再考虑到np.allclose(rtol=1e-05, atol=1e-08),所以将EPSILON改成1e-05
EPSILON = 1e-05
