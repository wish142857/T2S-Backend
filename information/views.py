import json
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
    if not check_necessary(_information_id):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
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
    # *** 参数获取 ***
    _information_id = request.POST.get('information_id')
    _information_state = request.POST.get('information_state')
    # *** 合法性检测 ***
    if not check_necessary(_information_id, _information_state):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_enumeration(_information_state, ('N', 'R', 'H')):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    user = request.user
    try:
        teacher = Teacher.objects.get(user=user)
        information = teacher.information_set.get(information_id=_information_id)
        information.information_state = _information_state
        information.save()
        response = {'status': True, 'info': S_UPDATE_SUCCEED}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except (Teacher.DoesNotExist, Information.DoesNotExist):
        pass
    try:
        student = Student.objects.get(user=user)
        information = student.information_set.get(information_id=_information_id)
        information.information_state = _information_state
        information.save()
        response = {'status': True, 'info': S_UPDATE_SUCCEED}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except (Student.DoesNotExist, Information.DoesNotExist):
        pass
    response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@ post_required
def create_information(request):
    # *** 参数获取 ***
    _receiver_type = request.POST.get('receiver_type')
    _receiver_id = request.POST.get('receiver_id')
    _information_type = request.POST.get('information_type')
    _information_content = request.POST.get('information_content')
    _information_state = request.POST.get('information_state')
    # *** 合法性检测 ***
    if not check_necessary(_receiver_type, _receiver_id, _information_type, _information_content, _information_state):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_enumeration(_receiver_type, ('T', 'S')) or not check_enumeration(_information_type, ('T', 'P')) or not check_enumeration(_information_state, ('N', 'R', 'H')):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    if _receiver_type == 'T':
        try:
            teacher = Teacher.objects.get(teacher_id=_receiver_id)
            Information.objects.create(
                receiver_teacher=teacher,
                receiver_type=_receiver_type,
                information_type=_information_type,
                information_state=_information_state,
                information_content=_information_content,
            )
            response = {'status': True, 'info': S_CREATE_SUCCEED}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Teacher.DoesNotExist:
            response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
    else:
        try:
            student = Student.objects.get(student_id=_receiver_id)
            Information.objects.create(
                receiver_student=student,
                receiver_type=_receiver_type,
                information_type=_information_type,
                information_state=_information_state,
                information_content=_information_content,
            )
            response = {'status': True, 'info': S_CREATE_SUCCEED}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Student.DoesNotExist:
            response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
            return HttpResponse(json.dumps(response, ensure_ascii=False))


@ post_required
def delete_information(request):
    # *** 参数获取 ***
    _information_id = request.POST.get('information_id')
    # *** 合法性检测 ***
    if not check_necessary(_information_id):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    try:
        Information.objects.get(information_id=_information_id).delete()
        response = {'status': True, 'info': S_DELETE_SUCCEED}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Information.DoesNotExist:
        response = {'status': False, 'info': F_DELETE_FAIL}
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@ post_required
def update_information(request):
    # *** 参数获取 ***
    _information_id = request.POST.get('information_id')
    _information_type = request.POST.get('information_type')
    _information_content = request.POST.get('information_content')
    _information_state = request.POST.get('information_state')
    # *** 合法性检测 ***
    if not check_necessary(_information_id) or not check_optional(_information_type, _information_content, _information_state):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_enumeration(_information_type, ('T', 'P')) or not check_enumeration(_information_state, ('N', 'R', 'H')):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    try:
        information = Information.objects.get(information_id=_information_id)
        if _information_type is not None:
            information.information_type = _information_type
        if _information_content is not None:
            information.information_content = _information_content
        if _information_state is not None:
            information._information_state = _information_state
        information.save()
        response = {'status': True, 'info': S_UPDATE_SUCCEED}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Information.DoesNotExist:
        response = {'status': False, 'info': F_UPDATE_FAIL}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
