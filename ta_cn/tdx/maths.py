#
# def SUB(*args):
#     """相减"""
#     return reduce(_np.subtract, args)
# def MUL(*args):
#     """连乘"""
#     return reduce(_np.multiply, args)
# def DIV(*args):
#     """连除
#     RuntimeWarning: invalid value encountered in true_divide
#     """
#     with _np.errstate(divide='ignore', invalid='ignore'):
#         return reduce(_np.true_divide, args)
# def MEAN(*args):
#     """均值"""
#     return ADD(*args) / len(args)
# def ROUND(a, decimals):
#     """四舍五入取3位小数
#     ROUND(a, decimals=3)
#     """
#     return _np.round(a, decimals)