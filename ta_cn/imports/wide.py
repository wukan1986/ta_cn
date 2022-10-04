"""
对指标的算子化包装
1. 包装成只支持 宽表 输入，输出是特殊格式，需要处理得到输出
2. 简化参数输入，命名参数也可当成位置参数输入
3. 通过堆叠的方法，自动跳过停牌

!!!函数太多，又想要智能提示，只能手工按需补充
"""
from ..alphas.alpha import CUMPROD
from ..alphas.alpha import FILTER_191
from ..regress import REGRESI
from ..regress import SLOPE_YX
from ..utils_wide import wide_wraps

#
CUMPROD = wide_wraps(CUMPROD, to_kwargs={})
FILTER_191 = wide_wraps(FILTER_191, input_num=2, to_kwargs={})



SLOPE_YX = wide_wraps(SLOPE_YX, input_num=2, to_kwargs={2: 'timeperiod'})
REGRESI4 = wide_wraps(REGRESI, input_num=4, to_kwargs={4: 'timeperiod'})

# 长表转宽表

