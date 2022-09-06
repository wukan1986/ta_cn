"""
Group Operators
"""


def group_backfill(x, group, d, std=4.0):
    """If a certain value for a certain date and instrument is NaN, from the set of same group instruments, calculate winsorized mean of all non-NaN values over last d days."""
    pass


def group_count(x, group):
    """Gives the number of instruments in the same group (e.g. sector) which have valid values of x. For example, x=1 gives the number of instruments in each group (without regard for whether any particular field has valid data)."""
    pass


def group_extra(x, weight, group):
    """Replaces NaN values by their corresponding group means."""
    pass


def group_max(x, group):
    """Maximum of x for all instruments in the same group."""
    pass


def group_mean(x, weight, group):
    """All elements in group equals to the mean value of the group. Mean = sum(data*weight) / sum(weight) in each group."""
    pass


def group_median(x, group):
    """All elements in group equals to the median value of the group."""
    pass


def group_min(x, group):
    """All elements in group equals to the min value of the group."""
    pass


def group_neutralize(x, group):
    """Neutralizes Alpha against groups. These groups can be subindustry, industry, sector, country or a constant."""
    pass


def group_normalize(x, group, constantCheck=False, tolerance=0.01, scale=1):
    """Normalizes input such that each group's absolute sum is 1."""
    pass


def group_percentage(x, group, percentage=0.5):
    """All elements in group equals to the value over the percentage of the group.
Percentage = 0.5 means value is equal to group_median(x, group)"""
    pass


def group_vector_proj(x, y, g):
    """
Similar to vector_proj(x, y) but x projection to y for each group which can be any classifier such as subindustry, industry, sector, etc. Refer wiki  for more details"""
    pass


def group_rank(x, group):
    """Each elements in a group is assigned the corresponding rank in this group"""
    pass


def group_scale(x, group):
    """Normalizes the values in a group to be between 0 and 1. (x - groupmin) / (groupmax - groupmin)"""
    pass


def group_std_dev(x, group):
    """All elements in group equals to the standard deviation of the group."""
    pass


def group_sum(x, group):
    """Sum of x for all instruments in the same group."""
    pass


def group_vector_neut(x, y, g):
    """Similar to vector_neut(x, y) but x neutralize to y for each group g which can be any classifier such as subindustry, industry, sector, etc."""
    pass


def group_zscore(x, group):
    """Calculates group Z-score - numerical measurement that describes a value's relationship to the mean of a group of values. Z-score is measured in terms of standard deviations from the mean. zscore = (data - mean) / stddev of x for each instrument within its group."""
    pass
