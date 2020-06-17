"""
通用函数
"""
import difflib

from intention.models import Recruitment, Application
from user.models import Teacher, Student


def main():
    s = set()
    a = ('q1', 'w1', 1)
    b = ('q2', 'w2', 2)
    c = ('q1', 'w1', 1)
    s.add(a)
    s.add(b)
    s.add(c)
    print(s)


if __name__ == '__main__':
    main()


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


# 计算匹配度  导师研究方向-招收意向研究方向
def calculate_match_degree_t2r(t: Teacher, r: Recruitment) -> int:
    return difflib.SequenceMatcher(None, t.research_fields, r.research_fields).quick_ratio()


# 计算匹配度  学生学位-招收意向招收类型   学生研究兴趣-招收意向研究方向
def calculate_match_degree_s2r(s: Student, r: Recruitment) -> int:
    ratio_1 = difflib.SequenceMatcher(None, s.degree, r.recruitment_type).quick_ratio()
    ratio_2 = difflib.SequenceMatcher(None, s.research_interest, r.research_fields).quick_ratio()
    return (ratio_1 + ratio_2) / 2


# 计算匹配度  导师研究方向-申请意向兴趣方向
def calculate_match_degree_t2a(t: Teacher, a: Application) -> int:
    return difflib.SequenceMatcher(None, t.research_fields, a.research_interests).quick_ratio()


# 计算匹配度  学生研究兴趣-申请意向兴趣方向
def calculate_match_degree_s2a(s: Student, a: Application) -> int:
    return difflib.SequenceMatcher(None, s.research_interest, a.research_interests).quick_ratio()
