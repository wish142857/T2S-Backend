import json
from django.shortcuts import render
from T2S_Backend.decorators import *
from T2S_Backend.globals import *
from T2S_Backend.utils import *
from user.models import Teacher, Student
from information.models import Information


@ get_required
@ login_required
def get_information(request):
    # *** 请求处理 ***
    user = request.user
    try:
        teacher = Teacher.objects.get(user=user)
        information_id_list = [i.information_id for i in teacher.information_set.all()]
        response = {'status': True, 'info': S_QUERY_SUCCEED, 'information_id_list': information_id_list}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        information_id_list = [i.information_id for i in student.information_set.all()]
        response = {'status': True, 'info': S_QUERY_SUCCEED, 'information_id_list': information_id_list}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Student.DoesNotExist:
        pass
    response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@ get_required
@ login_required
def get_information_detail(request):
    # *** 参数获取 ***
    _information_id = request.GET.get('information_id')
    # *** 合法性检测 ***
    if not check_none(_information_id):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_empty(_information_id):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    user = request.user
    try:
        teacher = Teacher.objects.get(user=user)
        information = teacher.information_set.get(information_id=_information_id)
        response = {
            'status': True,
            'info': S_QUERY_SUCCEED,
            'information_time': information.information_time,
            'information_type': information.information_type,
            'information_content': information.information_content,
            'information_state': information.information_state,
        }
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except (Teacher.DoesNotExist, Information.DoesNotExist):
        pass
    try:
        student = Student.objects.get(user=user)
        information = student.information_set.get(information_id=_information_id)
        response = {
            'status': True,
            'info': S_QUERY_SUCCEED,
            'information_time': information.information_time,
            'information_type': information.information_type,
            'information_content': information.information_content,
            'information_state': information.information_state,
        }
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except (Student.DoesNotExist, Information.DoesNotExist):
        pass
    response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@ post_required
@ login_required
def set_information_state(request):
    # TODO
    pass


@ post_required
def create_information(request):
    # TODO
    pass


@ post_required
def delete_information(request):
    # TODO
    pass


@ post_required
def update_information(request):
    # TODO
    pass
