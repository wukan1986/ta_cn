# 此处引入库要小心，有可能打破只想用talib二维库的需求

# ReferenceError: underlying object has vanished
# 如果出现上面错误，请改成False,并删除多个目录下的__pycache__
numba_cache = False

# 按股票分组，计算时序指标。注意，组内时序需要已经排序
BY_ASSET = 'asset'
# 按时间分组。计算横截面
BY_DATE = 'date'
# 横截面上进行行业中性化
BY_GROUP = ['date', 'group']
