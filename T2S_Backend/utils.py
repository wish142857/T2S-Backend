"""
通用函数
"""


def check_necessary(*args):
    for a in args:
        if a is None:
            return False
    return True


def check_optional(*args):
    for a in args:
        if a is not None:
            return True
    return False


def check_nonempty(*args):
    for a in args:
        if a is not None and len(a) == 0:
            return False
    return True


def check_enumeration(arg, choices):
    if arg is not None and arg not in choices:
        return False
    return True


def auth_teacher(teacher_number, id_number):
    # TODO
    return False


def auth_student(student_number, id_number):
    # TODO
    return False
