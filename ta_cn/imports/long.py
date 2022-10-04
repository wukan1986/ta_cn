"""
对指标的算子化包装
1. 包装成只支持 长表 输入和输出
2. 简化参数输入，命名参数也可当成位置参数输入
3. 通过dropna的方法，自动跳过停牌

!!!函数太多，又想要智能提示，只能手工按需补充
"""
from .. import BY_ASSET, BY_DATE, BY_GROUP
from ..aggregate import A_div_AB
from ..alphas.alpha import CUMPROD
from ..alphas.alpha import FILTER_191
from ..regress import REGRESI
from ..regress import SLOPE_YX
from ..utils_long import dataframe_groupby_apply, series_groupby_apply

# 特殊
CUMPROD = series_groupby_apply(CUMPROD, by=BY_ASSET, to_kwargs={})
FILTER_191 = dataframe_groupby_apply(FILTER_191, by=BY_ASSET, to_kwargs={}, dropna=False)
#


SLOPE_YX = dataframe_groupby_apply(SLOPE_YX, by=BY_ASSET)
REGRESI4 = dataframe_groupby_apply(REGRESI, by=BY_ASSET, to_df=[0, 1, 2, 3], to_kwargs={4: 'timeperiod'})

# 可用于 全部市场宽度
A_div_AB_1 = series_groupby_apply(A_div_AB, by=BY_DATE, to_kwargs={})
# 可用于 板块市场宽度
A_div_AB_2 = dataframe_groupby_apply(A_div_AB, by=BY_GROUP, to_df=[0, 'group'], to_kwargs={})
