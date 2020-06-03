"""
通用函数
"""
import difflib


def test():
    str1 = '广州公安'
    str2 = '广州公安市委市政府; asdasd; 21345214'
    str3 = '广州'
    return difflib.SequenceMatcher(None, str1, str2).quick_ratio()




def check_necessary(*args) -> bool:
    for a in args:
        if a is None:
            return False
    return True


def check_optional(*args) -> bool:
    for a in args:
        if a is not None:
            return True
    return False


def check_nonempty(*args) -> bool:
    for a in args:
        if a is not None and len(a) == 0:
            return False
    return True


def check_enumeration(arg, choices) -> bool:
    if arg is not None and arg not in choices:
        return False
    return True


def auth_teacher(teacher_number, id_number) -> bool:
    # TODO
    return False


def auth_student(student_number, id_number) -> bool:
    # TODO
    return False


def calculate_match_degree_t2s(t, s) -> int:
    return 0


def calculate_match_degree_s2t(s, t) -> int:
    return 0


def calculate_match_degree_t2t(t1, t2) -> int:
    return 0


def calculate_match_degree_s2s(s1, s2) -> int:
    return 0

