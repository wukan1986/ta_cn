"""宽表不好处理的算子，转成长表进行处理再还原"""
from ta_cn.utils import np_to_pd
from ta_cn.utils_wide import get_raw_arr, WArr
from .long import indneutralize as _indneutralize


def indneutralize(x, group):
    """行业中性化

    对宽表处理实在过于麻烦，所以将其转换成了长表
    """

    x1 = np_to_pd(get_raw_arr(x)).stack(dropna=False)
    g1 = np_to_pd(get_raw_arr(group)).stack(dropna=False)

    x1.index.names = ['date', 'asset']
    g1.index.names = ['date', 'asset']

    r = _indneutralize(x1, g1)

    return WArr.from_array(r.unstack(), direction=None)
