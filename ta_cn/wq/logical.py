"""
Logical Operators
"""
from functools import reduce

import numpy as np


def and_(*args):
    """Logical AND operator, returns true if both operands are true and returns false otherwise"""
    return reduce(lambda x, y: np.logical_and(x, y), list(args))


def or_(*args):
    """Logical OR operator returns true if either or both inputs are true and returns false otherwise"""
    return reduce(lambda x, y: np.logical_or(x, y), args)


def equal(input1, input2):
    """Returns true if both inputs are same and returns false otherwise"""
    return input1 == input2


def negate(input):
    """The result is true if the converted operand is false; the result is false if the converted operand is true"""
    return ~input


def less(input1, input2):
    """If input1 < input2 return true, else return false"""
    return input1 - input2 < 0


def if_else(input1, input2, input3):
    """If input1 is true then return input2 else return input3."""
    return np.where(input1, input2, input3)


def is_not_nan(input):
    """If (input != NaN) return 1 else return 0"""
    return input == input


def is_nan(input):
    """If (input == NaN) return 1 else return 0"""
    return input != input


def is_finite(input):
    """If (input NaN or input == INF) return 0, else return 1"""
    return np.isinf(input)


def is_not_finite(input):
    """If (input NAN or input == INF) return 1 else return 0"""
    return ~np.isinf(input)
