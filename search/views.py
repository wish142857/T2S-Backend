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
    teachers = Teacher.objects.filter(
        Q(account__icontains=_key) | Q(name__icontains=_key) |
        Q(school__icontains=_key) | Q(department__icontains=_key) |
        Q(introduction__icontains=_key) | Q(research_fields__icontains=_key)
    )
    teacher_info_list = []
    for t in teachers.all():
        teacher_info = {'teacher_id': t.teacher_id, 'name': t.name, 'school': t.school, 'department': t.department,
                        'fans_number': t.user.teacher_fans.count() + t.user.student_fans.count(), 'is_followed': False}
        try:
            follow_list.get(username=t.user.username)
            teacher_info['is_followed'] = True
        except User.DoesNotExist:
            pass
        teacher_info_list.append(teacher_info)
    response = {'status': True, 'info': S_SEARCH_SUCCEED, 'teacher_info_list': teacher_info_list}
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
    students = Student.objects.filter(
        Q(account__icontains=_key) | Q(name__icontains=_key) |
        Q(school__icontains=_key) | Q(department__icontains=_key) | Q(major__icontains=_key) |
        Q(introduction__icontains=_key) | Q(research_experience__icontains=_key)
    )
    student_info_list = []
    for s in students.all():
        student_info = {'student_id': s.student_id, 'name': s.name, 'school': s.school, 'department': s.department,
                        'fans_number': s.user.teacher_fans.count() + s.user.student_fans.count(), 'is_followed': False}
        try:
            follow_list.get(username=s.user.username)
            student_info['is_followed'] = True
        except User.DoesNotExist:
            pass
        student_info_list.append(student_info)
    response = {'status': True, 'info': S_SEARCH_SUCCEED, 'student_info_list': student_info_list}
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
    recruitment = Recruitment.objects.filter(
        Q(research_fields__icontains=_key) | Q(introduction__icontains=_key)
    )
    response = {'status': True, 'info': S_SEARCH_SUCCEED, 'recruitment_id_list': [r.recruitment_id for r in recruitment.all()]}
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
    application = Application.objects.filter(
        Q(research_interests__icontains=_key) | Q(introduction__icontains=_key)
    )
    response = {'status': True, 'info': S_SEARCH_SUCCEED, 'application_id_list': [a.application_id for a in application.all()]}
    return HttpResponse(json.dumps(response, ensure_ascii=False))
