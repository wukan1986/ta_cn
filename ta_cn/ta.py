import talib as ta

TA_COMPATIBILITY_DEFAULT = 0  # 使用MA做第一个值
TA_COMPATIBILITY_METASTOCK = 1  # 使用Price做第一个值

_COMPATIBILITY_ENABLE_ = False


def TA_SET_COMPATIBILITY_ENABLE(enable):
    global _COMPATIBILITY_ENABLE_
    _COMPATIBILITY_ENABLE_ = enable


def TA_SET_COMPATIBILITY(compatibility):
    global _COMPATIBILITY_ENABLE_
    if _COMPATIBILITY_ENABLE_:
        print('do ta.set_compatibility', compatibility)
        ta.set_compatibility(compatibility)
