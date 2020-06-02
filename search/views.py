import json

from django.db.models import Q
from T2S_Backend.decorators import *
from T2S_Backend.globals import *
from T2S_Backend.utils import *
from user.models import Teacher, Student
from intention.models import Recruitment, Application


@ get_required
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
    teachers = Teacher.objects.filter(
        Q(account__icontains=_key) | Q(name__icontains=_key) |
        Q(school__icontains=_key) | Q(department__icontains=_key) |
        Q(introduction__icontains=_key) | Q(research_fields__icontains=_key)
    )
    response = {'status': True, 'info': S_QUERY_SUCCEED, 'teacher_id_list': [t.teacher_id for t in teachers.all()]}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@ get_required
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
    students = Student.objects.filter(
        Q(account__icontains=_key) | Q(name__icontains=_key) |
        Q(school__icontains=_key) | Q(department__icontains=_key) | Q(major__icontains=_key) |
        Q(introduction__icontains=_key) | Q(research_experience__icontains=_key)
    )
    response = {'status': True, 'info': S_QUERY_SUCCEED, 'student_id_list': [s.student_id for s in students.all()]}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@ get_required
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
    response = {'status': True, 'info': S_QUERY_SUCCEED, 'recruitment_id_list': [r.recruitment_id for r in recruitment.all()]}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@ get_required
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
    response = {'status': True, 'info': S_QUERY_SUCCEED, 'application_id_list': [a.application_id for a in application.all()]}
    return HttpResponse(json.dumps(response, ensure_ascii=False))
