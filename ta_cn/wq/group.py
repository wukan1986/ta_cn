"""
Group Operators

分组计算
返回的组内是一个值，还是多个值？
1. group_count等等肯定是一个值。输出索引是date,group
2. group_rankt等等是输出多个值。输出索引是date,asset

"""
import numpy as np

from .. import BY_GROUP
from ..utils_long import dataframe_groupby_apply


def group_backfill(x, group, d, std=4.0):
    """If a certain value for a certain date and instrument is NaN, from the set of same group instruments, calculate winsorized mean of all non-NaN values over last d days."""
    pass


def group_count(x, group):
    """Gives the number of instruments in the same group (e.g. sector) which have valid values of x. For example, x=1 gives the number of instruments in each group (without regard for whether any particular field has valid data)."""
    func = dataframe_groupby_apply(len, by=BY_GROUP, to_df=[0, 'group'], to_kwargs={})

    return func(x, group)


def group_extra(x, weight, group):
    """Replaces NaN values by their corresponding group means."""
    pass
    # func = dataframe_groupby_apply(None, by=BY_GROUP, to_df=[0, 'group'], to_kwargs={}, dropna=False)
    #
    # return func(x, group)


def group_max(x, group):
    """Maximum of x for all instruments in the same group."""
    func = dataframe_groupby_apply(np.max, by=BY_GROUP, to_df=[0, 'group'], to_kwargs={})

    return func(x, group)


def group_mean(x, weight, group):
    """All elements in group equals to the mean value of the group. Mean = sum(data*weight) / sum(weight) in each group."""

    # TODO: 这里的权重是与x等长的权重序列，还是与股票数一样的权重？
    def _mean(x, weight):
        return np.average(x, weights=weight)

    func = dataframe_groupby_apply(_mean, by=BY_GROUP, to_df=[0, 1, 'group'], to_kwargs={})

    return func(x, weight, group)


def group_median(x, group):
    """All elements in group equals to the median value of the group."""
    func = dataframe_groupby_apply(np.median, by=BY_GROUP, to_df=[0, 'group'], to_kwargs={})

    return func(x, group)


def group_min(x, group):
    """All elements in group equals to the min value of the group."""
    func = dataframe_groupby_apply(np.min, by=BY_GROUP, to_df=[0, 'group'], to_kwargs={})

    return func(x, group)


def group_neutralize(x, group):
    """Neutralizes Alpha against groups. These groups can be subindustry, industry, sector, country or a constant."""

    def _demean(x):
        """行业中性化，需要与groupby配合使用

        RuntimeWarning: Mean of empty slice
        nanmean在全nan时报此警告。这个警告还不好屏蔽
        """
        return x - np.nanmean(x)

    func = dataframe_groupby_apply(_demean, by=BY_GROUP, to_df=[0, 'group'], to_kwargs={})

    return func(x, group)


def group_normalize(x, group, constantCheck=False, tolerance=0.01, scale=1):
    """Normalizes input such that each group's absolute sum is 1."""

    # 发现这里的group_normalize其实像scale，也就是不少地方混乱
    def _normalize(x, scale):
        sum_x = np.sum(abs(x))
        return x / sum_x * scale

    func = dataframe_groupby_apply(_normalize, by=BY_GROUP, to_df=[0, 'group'], to_kwargs={2: 'scale'})

    return func(x, group, scale)


def group_percentage(x, group, percentage=0.5):
    """All elements in group equals to the value over the percentage of the group.
Percentage = 0.5 means value is equal to group_median(x, group)"""

    func = dataframe_groupby_apply(np.quantile, by=BY_GROUP, to_df=[0, 'group'], to_kwargs={2: 'q'})

    return func(x, group, percentage)


def group_vector_proj(x, y, g):
    """
Similar to vector_proj(x, y) but x projection to y for each group which can be any classifier such as subindustry, industry, sector, etc. Refer wiki  for more details"""
    pass


def group_rank(x, group):
    """Each elements in a group is assigned the corresponding rank in this group"""
    func = dataframe_groupby_apply(lambda x: x.rank(pct=True), by=BY_GROUP, to_df=[0, 'group'], to_kwargs={})

    return func(x, group)


def group_scale(x, group):
    """Normalizes the values in a group to be between 0 and 1. (x - groupmin) / (groupmax - groupmin)"""

    def _scale(x):
        t1 = np.min(x)
        t2 = np.max(x)
        return (x - t1) / (t2 - t1)

    func = dataframe_groupby_apply(_scale, by=BY_GROUP, to_df=[0, 'group'], to_kwargs={})

    return func(x, group)


def group_std_dev(x, group):
    """All elements in group equals to the standard deviation of the group."""

    func = dataframe_groupby_apply(np.std, by=BY_GROUP, to_df=[0, 'group'], to_kwargs={})

    return func(x, group)


def group_sum(x, group):
    """Sum of x for all instruments in the same group."""
    func = dataframe_groupby_apply(np.sum, by=BY_GROUP, to_df=[0, 'group'], to_kwargs={})

    return func(x, group)


def group_vector_neut(x, y, g):
    """Similar to vector_neut(x, y) but x neutralize to y for each group g which can be any classifier such as subindustry, industry, sector, etc."""
    pass


def group_zscore(x, group):
    """Calculates group Z-score - numerical measurement that describes a value's relationship to the mean of a group of values. Z-score is measured in terms of standard deviations from the mean. zscore = (data - mean) / stddev of x for each instrument within its group."""

    def _zscore(x):
        return (x - np.mean(x)) / np.std(x)

    func = dataframe_groupby_apply(_zscore, by=BY_GROUP, to_df=[0, 'group'], to_kwargs={})

    return func(x, group)
