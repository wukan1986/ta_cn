from functools import wraps

import bottleneck as _bn
import numpy as np


def bn_move_window(func):
    """bottleneck在数据量少返回nan"""

    @wraps(func)
    def decorated(a, window, *args, axis=-1, **kwargs):
        if a.shape[axis] < window:
            return np.full_like(a, fill_value=np.nan)
        return func(a, window, *args, axis=axis, **kwargs)

    return decorated


move_argmax = bn_move_window(_bn.move_argmax)
move_argmin = bn_move_window(_bn.move_argmin)
move_max = bn_move_window(_bn.move_max)
move_mean = bn_move_window(_bn.move_mean)
move_median = bn_move_window(_bn.move_median)
move_min = bn_move_window(_bn.move_min)
move_rank = bn_move_window(_bn.move_rank)
move_std = bn_move_window(_bn.move_std)
move_sum = bn_move_window(_bn.move_sum)
move_var = bn_move_window(_bn.move_var)
