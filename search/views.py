import json

from django.contrib.auth.models import User
from django.db.models import Q
from T2S_Backend.decorators import *
from T2S_Backend.globals import *
from T2S_Backend.utils import *
from user.models import Teacher, Student
from intention.models import Recruitment, Application


@get_required
@login_required
def search_teacher(request):
    # *** 参数获取 ***
    _key = request.GET.get('key')
    # *** 合法性检测 ***
    if not check_necessary(_key):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_nonempty(_key):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    # 获取用户关注列表
    user = request.user
    follow_list = None
    try:
        follow_list = Teacher.objects.get(user=user).follows
    except Teacher.DoesNotExist:
        pass
    try:
        follow_list = Student.objects.get(user=user).follows
    except Student.DoesNotExist:
        pass
    if follow_list is None:
        response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # 进行关键字搜索
    teachers = Teacher.objects.filter(
        Q(account__icontains=_key) | Q(name__icontains=_key) |
        Q(school__icontains=_key) | Q(department__icontains=_key) |
        Q(introduction__icontains=_key) | Q(research_fields__icontains=_key)
    )
    if teachers.all().count() == 0:
        response = {'status': False, 'info': F_ERROR_NOT_FOUND}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    try:
        teacher = Teacher.objects.get(user=user)
        teacher_info_list = []
        for t in teachers.all():
            teacher_info = {'teacher_id': t.teacher_id, 'name': t.name, 'gender': t.gender, 'school': t.school, 'department': t.department,
                            'auth_state': t.auth_state, 'fans_number': t.user.teacher_fans.count() + t.user.student_fans.count(),
                            'is_followed': False, 'match_degree': calculate_match_degree_t2t(teacher, t)}
            try:
                follow_list.get(username=t.user.username)
                teacher_info['is_followed'] = True
            except User.DoesNotExist:
                pass
            teacher_info_list.append(teacher_info)
        response = {'status': True, 'info': S_SEARCH_SUCCEED, 'teacher_info_list': teacher_info_list}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        teacher_info_list = []
        for t in teachers.all():
            teacher_info = {'teacher_id': t.teacher_id, 'name': t.name, 'gender': t.gender, 'school': t.school,
                            'department': t.department, 'auth_state': t.auth_state, 'fans_number': t.user.teacher_fans.count() + t.user.student_fans.count(),
                            'is_followed': False, 'match_degree': calculate_match_degree_s2t(student, t)}
            try:
                follow_list.get(username=t.user.username)
                teacher_info['is_followed'] = True
            except User.DoesNotExist:
                pass
            teacher_info_list.append(teacher_info)
        response = {'status': True, 'info': S_SEARCH_SUCCEED, 'teacher_info_list': teacher_info_list}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Student.DoesNotExist:
        pass
    response = {'status': False, 'info': F_ERROR_NOT_FOUND}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
@login_required
def search_student(request):
    # *** 参数获取 ***
    _key = request.GET.get('key')
    # *** 合法性检测 ***
    if not check_necessary(_key):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_nonempty(_key):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    # 获取用户关注列表
    user = request.user
    follow_list = None
    try:
        follow_list = Teacher.objects.get(user=user).follows
    except Teacher.DoesNotExist:
        pass
    try:
        follow_list = Student.objects.get(user=user).follows
    except Student.DoesNotExist:
        pass
    if follow_list is None:
        response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # 进行关键字搜索
    students = Student.objects.filter(
        Q(account__icontains=_key) | Q(name__icontains=_key) |
        Q(school__icontains=_key) | Q(department__icontains=_key) | Q(major__icontains=_key) |
        Q(introduction__icontains=_key) | Q(research_experience__icontains=_key)
    )
    if students.all().count() == 0:
        response = {'status': False, 'info': F_ERROR_NOT_FOUND}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    try:
        teacher = Teacher.objects.get(user=user)
        student_info_list = []
        for s in students.all():
            student_info = {'student_id': s.student_id, 'name': s.name, 'gender': s.gender, 'school': s.school,
                            'department': s.department, 'auth_state': s.auth_state, 'fans_number': s.user.teacher_fans.count() + s.user.student_fans.count(),
                            'is_followed': False, 'match_degree': calculate_match_degree_t2s(teacher, s)}
            try:
                follow_list.get(username=s.user.username)
                student_info['is_followed'] = True
            except User.DoesNotExist:
                pass
            student_info_list.append(student_info)
        response = {'status': True, 'info': S_SEARCH_SUCCEED, 'student_info_list': student_info_list}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        student_info_list = []
        for s in students.all():
            student_info = {'student_id': s.student_id, 'name': s.name, 'gender': s.gender, 'school': s.school,
                            'department': s.department, 'auth_state': s.auth_state, 'fans_number': s.user.teacher_fans.count() + s.user.student_fans.count(),
                            'is_followed': False, 'match_degree': calculate_match_degree_s2s(student, s)}
            try:
                follow_list.get(username=s.user.username)
                student_info['is_followed'] = True
            except User.DoesNotExist:
                pass
            student_info_list.append(student_info)
        response = {'status': True, 'info': S_SEARCH_SUCCEED, 'student_info_list': student_info_list}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Student.DoesNotExist:
        pass
    response = {'status': False, 'info': F_ERROR_NOT_FOUND}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
@login_required
def search_recruit_intention(request):
    # *** 参数获取 ***
    _key = request.GET.get('key')
    # *** 合法性检测 ***
    if not check_necessary(_key):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_nonempty(_key):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    recruitments = Recruitment.objects.filter(
        Q(research_fields__icontains=_key) | Q(introduction__icontains=_key)
    )
    if recruitments.all().count() == 0:
        response = {'status': False, 'info': F_ERROR_NOT_FOUND}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    response = {'status': True, 'info': S_SEARCH_SUCCEED, 'recruitment_id_list': [r.recruitment_id for r in recruitments.all()]}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
@login_required
def search_apply_intention(request):
    # *** 参数获取 ***
    _key = request.GET.get('key')
    # *** 合法性检测 ***
    if not check_necessary(_key):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_nonempty(_key):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    applications = Application.objects.filter(
        Q(research_interests__icontains=_key) | Q(introduction__icontains=_key)
    )
    if applications.all().count() == 0:
        response = {'status': False, 'info': F_ERROR_NOT_FOUND}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    response = {'status': True, 'info': S_SEARCH_SUCCEED, 'application_id_list': [a.application_id for a in applications.all()]}
    return HttpResponse(json.dumps(response, ensure_ascii=False))
