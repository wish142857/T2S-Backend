import json
from T2S_Backend.decorators import *
from T2S_Backend.globals import *
from T2S_Backend.utils import *
from user.models import Teacher, Student
from conversation.models import Message


@ get_required
@ login_required
def get_message(request):
    # *** 请求处理 ***
    user = request.user
    try:
        teacher = Teacher.objects.get(user=user)
        message_id = max(teacher.s_messages.last().message_id, teacher.r_messages.last().message_id)
        response = {'status': True, 'info': S_QUERY_SUCCEED, 'message_id': message_id}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        message_id = max(student.s_messages.last().message_id, student.r_messages.last().message_id)
        response = {'status': True, 'info': S_QUERY_SUCCEED, 'message_id': message_id}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Student.DoesNotExist:
        pass
    response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@ get_required
@ login_required
def get_new_messages(request):
    # *** 参数获取 ***
    _message_id = request.GET.get('message_id')
    # *** 合法性检测 ***
    if not check_necessary(_message_id):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    user = request.user
    try:
        teacher = Teacher.objects.get(user=user)
        message_id_list = [m.message_id for m in teacher.s_messages.filter(message_id__gt=_message_id)]
        message_id_list.extend([m.message_id for m in teacher.r_messages.filter(message_id__gt=_message_id)])
        message_id_list.sort()
        response = {'status': True, 'info': S_QUERY_SUCCEED, 'message_id_list': message_id_list}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        message_id_list = [m.message_id for m in student.s_messages.filter(message_id__gt=_message_id)]
        message_id_list.extend([m.message_id for m in student.r_messages.filter(message_id__gt=_message_id)])
        message_id_list.sort()
        response = {'status': True, 'info': S_QUERY_SUCCEED, 'message_id_list': message_id_list}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Student.DoesNotExist:
        pass
    response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@ get_required
@ login_required
def get_all_messages(request):
    # *** 请求处理 ***
    user = request.user
    try:
        teacher = Teacher.objects.get(user=user)
        message_id_list = [m.message_id for m in teacher.s_messages.all()]
        message_id_list.extend([m.message_id for m in teacher.r_messages.all()])
        message_id_list.sort()
        response = {'status': True, 'info': S_QUERY_SUCCEED, 'message_id_list': message_id_list}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        message_id_list = [m.message_id for m in student.s_messages.all()]
        message_id_list.extend([m.message_id for m in student.r_messages.all()])
        message_id_list.sort()
        response = {'status': True, 'info': S_QUERY_SUCCEED, 'message_id_list': message_id_list}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Student.DoesNotExist:
        pass
    response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@ get_required
@ login_required
def get_message_detail(request):
    # *** 参数获取 ***
    _message_id = request.GET.get('message_id')
    # *** 合法性检测 ***
    if not check_necessary(_message_id):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    user = request.user
    try:
        message = Message.objects.get(message_id=_message_id)
    except Message.DoesNotExist:
        response = {'status': False, 'info': F_ERROR_NOT_FOUND}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    try:
        teacher = Teacher.objects.get(user=user)
        if message.sender_teacher == teacher:
            response = {
                'status': True,
                'info': S_QUERY_SUCCEED,
                'message_way': 'S',
                'message_type': message.message_type,
                'message_content': message.message_content,
                'message_time': message.message_time,
            }
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        if message.receiver_teacher == teacher:
            response = {
                'status': True,
                'info': S_QUERY_SUCCEED,
                'message_way': 'R',
                'message_type': message.message_type,
                'message_content': message.message_content,
                'message_time': message.message_time,
            }
            return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        if message.sender_student == student:
            response = {
                'status': True,
                'info': S_QUERY_SUCCEED,
                'message_way': 'S',
                'message_type': message.message_type,
                'message_content': message.message_content,
                'message_time': message.message_time,
            }
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        if message.receiver_student == student:
            response = {
                'status': True,
                'info': S_QUERY_SUCCEED,
                'message_way': 'R',
                'message_type': message.message_type,
                'message_content': message.message_content,
                'message_time': message.message_time,
            }
            return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Student.DoesNotExist:
        pass
    response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@ post_required
@ login_required
def send_message(request):
    # *** 参数获取 ***
    _object_id = request.POST.get('object_id')
    _object_type = request.POST.get('object_type')
    _message_type = request.POST.get('message_type')
    _message_content = request.POST.get('message_content')
    # *** 合法性检测 ***
    if not check_necessary(_object_id, _object_type, _message_type, _message_content):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_enumeration(_object_type, ('T', 'S')) or not check_enumeration(_message_type, ('T', 'P')):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    user = request.user
    try:
        teacher = Teacher.objects.get(user=user)
        if _object_type == 'T':
            t = Teacher.objects.get(teacher_id=_object_id)
            Message.objects.create(
                sender_teacher=teacher,
                receiver_teacher=t,
                sender_type='T',
                receiver_type='T',
                message_type=_message_type,
                message_content=_message_content,
            )
        else:
            s = Student.objects.get(student_id=_object_id)
            Message.objects.create(
                sender_teacher=teacher,
                receiver_student=s,
                sender_type='T',
                receiver_type='S',
                message_type=_message_type,
                message_content=_message_content,
            )
        response = {'status': True, 'info': S_SEND_SUCCEED}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except (Teacher.DoesNotExist, Student.DoesNotExist):
        pass
    try:
        student = Student.objects.get(user=user)
        if _object_type == 'T':
            t = Teacher.objects.get(teacher_id=_object_id)
            Message.objects.create(
                sender_student=student,
                receiver_teacher=t,
                sender_type='S',
                receiver_type='T',
                message_type=_message_type,
                message_content=_message_content,
            )
        else:
            s = Student.objects.get(student_id=_object_id)
            Message.objects.create(
                sender_student=student,
                receiver_student=s,
                sender_type='S',
                receiver_type='S',
                message_type=_message_type,
                message_content=_message_content,
            )
        response = {'status': True, 'info': S_SEND_SUCCEED}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except (Teacher.DoesNotExist, Student.DoesNotExist):
        pass
    response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
    return HttpResponse(json.dumps(response, ensure_ascii=False))
