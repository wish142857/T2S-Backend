"""
通用函数
"""


def check_none(*args):
    for a in args:
        if a is None:
            return False
    return True


def check_empty(*args):
    for a in args:
        if len(a) == 0:
            return False
    return True


def check_enum(arg, choices):
    if arg not in choices:
        return False
    return True
