"""
通用函数
"""
import difflib
from user.models import Teacher, Student

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


# 计算匹配度  导师院系-学生院系  导师研究方向-学生研究兴趣
def calculate_match_degree_t2s(t: Teacher, s: Student) -> int:
    ratio_1 = difflib.SequenceMatcher(None, t.department, s.department).quick_ratio()
    ratio_2 = difflib.SequenceMatcher(None, t.research_fields, s.research_interest).quick_ratio()
    return ratio_1 + ratio_2


# 计算匹配度  学生院系-导师院系  学生研究兴趣-导师研究方向
def calculate_match_degree_s2t(s: Student, t: Teacher) -> int:
    ratio_1 = difflib.SequenceMatcher(None, s.department, t.department).quick_ratio()
    ratio_2 = difflib.SequenceMatcher(None, s.research_interest, t.research_fields).quick_ratio()
    return ratio_1 + ratio_2


# 计算匹配度  导师院系-导师院系  导师研究方向-导师研究方向
def calculate_match_degree_t2t(t1: Teacher, t2: Teacher) -> int:
    ratio_1 = difflib.SequenceMatcher(None, t1.department, t2.department).quick_ratio()
    ratio_2 = difflib.SequenceMatcher(None, t1.research_fields, t2.research_fields).quick_ratio()
    return ratio_1 + ratio_2


# 计算匹配度  学生院系-学生院系  学生研究兴趣-学生研究兴趣
def calculate_match_degree_s2s(s1: Student, s2: Student) -> int:
    ratio_1 = difflib.SequenceMatcher(None, s1.department, s2.department).quick_ratio()
    ratio_2 = difflib.SequenceMatcher(None, s1.research_interest, s2.research_interest).quick_ratio()
    return ratio_1 + ratio_2
