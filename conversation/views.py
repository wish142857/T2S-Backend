import json
from T2S_Backend.decorators import *
from T2S_Backend.globals import *
from T2S_Backend.utils import *
from user.models import Teacher, Student
from conversation.models import Message


@get_required
@login_required
def get_conversation(request):
    # *** 请求处理 ***
    user = request.user
    conversation_set = set()
    try:
        teacher = Teacher.objects.get(user=user)
        for m in teacher.s_messages.all():
            if m.receiver_type == 'T':
                conversation = ('T', m.receiver_teacher.teacher_id, m.receiver_teacher.account, m.receiver_teacher.name)
                conversation_set.add(conversation)
            else:
                conversation = ('S', m.receiver_student.student_id, m.receiver_student.account, m.receiver_student.name)
                conversation_set.add(conversation)
        for m in teacher.r_messages.all():
            if m.sender_type == 'T':
                conversation = ('T', m.sender_teacher.teacher_id, m.sender_teacher.account, m.sender_teacher.name)
                conversation_set.add(conversation)
            else:
                conversation = ('S', m.sender_student.student_id, m.sender_student.account, m.sender_student.name)
                conversation_set.add(conversation)
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        for m in student.s_messages.all():
            if m.receiver_type == 'T':
                conversation = ('T', m.receiver_teacher.teacher_id, m.receiver_teacher.account, m.receiver_teacher.name)
                conversation_set.add(conversation)
            else:
                conversation = ('S', m.receiver_student.student_id, m.receiver_student.account, m.receiver_student.name)
                conversation_set.add(conversation)
        for m in student.r_messages.all():
            if m.sender_type == 'T':
                conversation = ('T', m.sender_teacher.teacher_id, m.sender_teacher.account, m.sender_teacher.name)
                conversation_set.add(conversation)
            else:
                conversation = ('S', m.sender_student.student_id, m.sender_student.account, m.sender_student.name)
                conversation_set.add(conversation)
    except Student.DoesNotExist:
        pass
    conversation_list = []
    for c in conversation_set:
        conversation_list.append({'object_type': c[0], 'object_id': c[1], 'object_account': c[2], 'object_name': c[3]})
    response = {'status': True, 'info': S_QUERY_SUCCEED, 'conversation_list': conversation_list}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
@login_required
def get_message(request):
    # *** 请求处理 ***
    user = request.user
    try:
        teacher = Teacher.objects.get(user=user)
        if teacher.s_messages.last() is None:
            x = -1
        else:
            x = teacher.s_messages.last().message_id
        if teacher.r_messages.last() is None:
            y = -1
        else:
            y = teacher.r_messages.last().message_id
        message_id = max(x, y)
        response = {'status': True, 'info': S_QUERY_SUCCEED, 'message_id': message_id}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        if student.s_messages.last() is None:
            x = -1
        else:
            x = student.s_messages.last().message_id
        if student.r_messages.last() is None:
            y = -1
        else:
            y = student.r_messages.last().message_id
        message_id = max(x, y)
        response = {'status': True, 'info': S_QUERY_SUCCEED, 'message_id': message_id}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Student.DoesNotExist:
        pass
    response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
@login_required
def get_new_messages(request):
    # *** 参数获取 ***
    _message_id = request.GET.get('message_id')
    # *** 合法性检测 ***
    if not check_necessary(_message_id):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    user = request.user
    s_messages = None
    r_messages = None
    try:
        teacher = Teacher.objects.get(user=user)
        s_messages = teacher.s_messages.filter(message_id__gt=_message_id)
        r_messages = teacher.r_messages.filter(message_id__gt=_message_id)
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        s_messages = student.s_messages.filter(message_id__gt=_message_id)
        r_messages = student.r_messages.filter(message_id__gt=_message_id)
    except Student.DoesNotExist:
        pass
    if s_messages is None or r_messages is None:
        response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    message_info_list = []
    for message in s_messages:
        message_info = {
            'message_id': message.message_id,
            'object_type': message.receiver_type,
            'object_id': None,
            'object_account': None,
            'object_name': None,
            'message_way': 'S',
            'message_type': message.message_type,
            'message_content': None,
            'message_time': message.message_time.strftime('%Y-%m-%d %H:%M'),
        }
        if message_info['object_type'] == 'T':
            message_info['object_id'] = message.receiver_teacher.teacher_id
            message_info['object_account'] = message.receiver_teacher.account
            message_info['object_name'] = message.receiver_teacher.name
        else:
            message_info['object_id'] = message.receiver_student.student_id
            message_info['object_account'] = message.receiver_student.account
            message_info['object_name'] = message.receiver_student.name
        if message.message_type == 'T':
            message_info['message_content'] = str(message.message_content, encoding="utf-8")
        elif message.message_type == 'P':
            message_info['message_content'] = '[图片]'
        message_info_list.append(message_info)
    for message in r_messages:
        message_info = {
            'message_id': message.message_id,
            'object_type': message.sender_type,
            'object_id': None,
            'object_account': None,
            'object_name': None,
            'message_way': 'R',
            'message_type': message.message_type,
            'message_content': None,
            'message_time': message.message_time.strftime('%Y-%m-%d %H:%M'),
        }
        if message_info['object_type'] == 'T':
            message_info['object_id'] = message.sender_teacher.teacher_id
            message_info['object_account'] = message.sender_teacher.account
            message_info['object_name'] = message.sender_teacher.name
        else:
            message_info['object_id'] = message.sender_student.student_id
            message_info['object_account'] = message.sender_student.account
            message_info['object_name'] = message.sender_student.name
        if message.message_type == 'T':
            message_info['message_content'] = str(message.message_content, encoding="utf-8")
        elif message.message_type == 'P':
            message_info['message_content'] = '[图片]'
        message_info_list.append(message_info)
    message_info_list.sort(key=lambda m: m['message_id'])
    response = {'status': True, 'info': S_QUERY_SUCCEED, 'message_info_list': message_info_list}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
@login_required
def get_all_messages(request):
    # *** 请求处理 ***
    user = request.user
    s_messages = None
    r_messages = None
    try:
        teacher = Teacher.objects.get(user=user)
        s_messages = teacher.s_messages.all()
        r_messages = teacher.r_messages.all()
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        s_messages = student.s_messages.all()
        r_messages = student.r_messages.all()
    except Student.DoesNotExist:
        pass
    if s_messages is None or r_messages is None:
        response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    message_info_list = []
    for message in s_messages:
        message_info = {
            'message_id': message.message_id,
            'object_type': message.receiver_type,
            'object_id': None,
            'object_account': None,
            'object_name': None,
            'message_way': 'S',
            'message_type': message.message_type,
            'message_content': None,
            'message_time': message.message_time.strftime('%Y-%m-%d %H:%M'),
        }
        if message_info['object_type'] == 'T':
            message_info['object_id'] = message.receiver_teacher.teacher_id
            message_info['object_account'] = message.receiver_teacher.account
            message_info['object_name'] = message.receiver_teacher.name
        else:
            message_info['object_id'] = message.receiver_student.student_id
            message_info['object_account'] = message.receiver_student.account
            message_info['object_name'] = message.receiver_student.name
        if message.message_type == 'T':
            message_info['message_content'] = str(message.message_content, encoding="utf-8")
        elif message.message_type == 'P':
            message_info['message_content'] = '[图片]'
        message_info_list.append(message_info)
    for message in r_messages:
        message_info = {
            'message_id': message.message_id,
            'object_type': message.sender_type,
            'object_id': None,
            'object_account': None,
            'object_name': None,
            'message_way': 'R',
            'message_type': message.message_type,
            'message_content': None,
            'message_time': message.message_time.strftime('%Y-%m-%d %H:%M'),
        }
        if message_info['object_type'] == 'T':
            message_info['object_id'] = message.sender_teacher.teacher_id
            message_info['object_account'] = message.sender_teacher.account
            message_info['object_name'] = message.sender_teacher.name
        else:
            message_info['object_id'] = message.sender_student.student_id
            message_info['object_account'] = message.sender_student.account
            message_info['object_name'] = message.sender_student.name
        if message.message_type == 'T':
            message_info['message_content'] = str(message.message_content, encoding="utf-8")
        elif message.message_type == 'P':
            message_info['message_content'] = '[图片]'
        message_info_list.append(message_info)
    message_info_list.sort(key=lambda m: m['message_id'])
    response = {'status': True, 'info': S_QUERY_SUCCEED, 'message_info_list': message_info_list}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
@login_required
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
                'object_type': message.receiver_type,
                'object_id': None,
                'object_account': None,
                'object_name': None,
                'message_way': 'S',
                'message_type': message.message_type,
                'message_content': None,
                'message_time': message.message_time.strftime('%Y-%m-%d %H:%M'),
            }
            if response['object_type'] == 'T':
                response['object_id'] = message.receiver_teacher.teacher_id
                response['object_account'] = message.receiver_teacher.account
                response['object_name'] = message.receiver_teacher.name
            else:
                response['object_id'] = message.receiver_student.student_id
                response['object_account'] = message.receiver_student.account
                response['object_name'] = message.receiver_student.name
            if message.message_type == 'T':
                response['message_content'] = str(message.message_content, encoding="utf-8")
            elif message.message_type == 'P':
                response['message_content'] = '[图片]'
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        if message.receiver_teacher == teacher:
            response = {
                'status': True,
                'info': S_QUERY_SUCCEED,
                'object_type': message.sender_type,
                'object_id': None,
                'object_account': None,
                'object_name': None,
                'message_way': 'R',
                'message_type': message.message_type,
                'message_content': None,
                'message_time': message.message_time.strftime('%Y-%m-%d %H:%M'),
            }
            if response['object_type'] == 'T':
                response['object_id'] = message.sender_teacher.teacher_id
                response['object_account'] = message.sender_teacher.account
                response['object_name'] = message.sender_teacher.name
            else:
                response['object_id'] = message.sender_student.student_id
                response['object_account'] = message.sender_student.account
                response['object_name'] = message.sender_student.name
            if message.message_type == 'T':
                response['message_content'] = str(message.message_content, encoding="utf-8")
            elif message.message_type == 'P':
                response['message_content'] = '[图片]'
            return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        if message.sender_student == student:
            response = {
                'status': True,
                'info': S_QUERY_SUCCEED,
                'object_type': message.receiver_type,
                'object_id': None,
                'object_account': None,
                'object_name': None,
                'message_way': 'S',
                'message_type': message.message_type,
                'message_content': None,
                'message_time': message.message_time.strftime('%Y-%m-%d %H:%M'),
            }
            if response['object_type'] == 'T':
                response['object_id'] = message.receiver_teacher.teacher_id
                response['object_account'] = message.receiver_teacher.account
                response['object_name'] = message.receiver_teacher.name
            else:
                response['object_id'] = message.receiver_student.student_id
                response['object_account'] = message.receiver_student.account
                response['object_name'] = message.receiver_student.name
            if message.message_type == 'T':
                response['message_content'] = str(message.message_content, encoding="utf-8")
            elif message.message_type == 'P':
                response['message_content'] = '[图片]'
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        if message.receiver_student == student:
            response = {
                'status': True,
                'info': S_QUERY_SUCCEED,
                'object_type': message.sender_type,
                'object_id': None,
                'object_account': None,
                'object_name': None,
                'message_way': 'R',
                'message_type': message.message_type,
                'message_content': None,
                'message_time': message.message_time.strftime('%Y-%m-%d %H:%M'),
            }
            if response['object_type'] == 'T':
                response['object_id'] = message.sender_teacher.teacher_id
                response['object_account'] = message.sender_teacher.account
                response['object_name'] = message.sender_teacher.name
            else:
                response['object_id'] = message.sender_student.student_id
                response['object_account'] = message.sender_student.account
                response['object_name'] = message.sender_student.name
            if message.message_type == 'T':
                response['message_content'] = str(message.message_content, encoding="utf-8")
            elif message.message_type == 'P':
                response['message_content'] = '[图片]'
            return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Student.DoesNotExist:
        pass
    response = {'status': False, 'info': F_ERROR_NOT_FOUND}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
def get_message_picture(request):
    # *** 参数获取 ***
    _message_id = request.GET.get('message_id')
    # *** 合法性检测 ***
    if not check_necessary(_message_id):
        return HttpResponse(None, content_type='image/jpeg')
    # *** 请求处理 ***
    try:
        message = Message.objects.get(message_id=_message_id)
    except Message.DoesNotExist:
        return HttpResponse(None, content_type='image/jpeg')
    if not message.message_type == 'P':
        return HttpResponse(None, content_type='image/jpeg')
    return HttpResponse(message.message_content, content_type='image/jpeg')


@post_required
@login_required
def send_message(request):
    # *** 参数获取 ***
    _object_id = request.POST.get('object_id')
    _object_type = request.POST.get('object_type')
    _message_type = request.POST.get('message_type')
    # *** 合法性检测 ***
    if not check_necessary(_object_id, _object_type, _message_type):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_enumeration(_object_type, ('T', 'S')) or not check_enumeration(_message_type, ('T', 'P')):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    user = request.user
    if _message_type == 'T':
        # 上传文字
        _message_content = request.POST.get('message_content')
        if _message_content is None:
            response = {'status': False, 'info': F_MISSING_PARAMETER}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
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
                    message_content=bytes(_message_content, encoding="utf8"),
                )
            else:
                s = Student.objects.get(student_id=_object_id)
                Message.objects.create(
                    sender_teacher=teacher,
                    receiver_student=s,
                    sender_type='T',
                    receiver_type='S',
                    message_type=_message_type,
                    message_content=bytes(_message_content, encoding="utf8"),
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
                    message_content=bytes(_message_content, encoding="utf8"),
                )
            else:
                s = Student.objects.get(student_id=_object_id)
                Message.objects.create(
                    sender_student=student,
                    receiver_student=s,
                    sender_type='S',
                    receiver_type='S',
                    message_type=_message_type,
                    message_content=bytes(_message_content, encoding="utf8"),
                )
            response = {'status': True, 'info': S_SEND_SUCCEED}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except (Teacher.DoesNotExist, Student.DoesNotExist):
            pass
    if _message_type == 'P':
        # 上传图片
        _message_content = request.FILES.get('message_content')
        if _message_content is None:
            response = {'status': False, 'info': F_MISSING_PARAMETER}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
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
                    message_content=_message_content.read(),
                )
            else:
                s = Student.objects.get(student_id=_object_id)
                Message.objects.create(
                    sender_teacher=teacher,
                    receiver_student=s,
                    sender_type='T',
                    receiver_type='S',
                    message_type=_message_type,
                    message_content=_message_content.read(),
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
                    message_content=_message_content.read(),
                )
            else:
                s = Student.objects.get(student_id=_object_id)
                Message.objects.create(
                    sender_student=student,
                    receiver_student=s,
                    sender_type='S',
                    receiver_type='S',
                    message_type=_message_type,
                    message_content=_message_content.read(),
                )
            response = {'status': True, 'info': S_SEND_SUCCEED}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except (Teacher.DoesNotExist, Student.DoesNotExist):
            pass
    response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
    return HttpResponse(json.dumps(response, ensure_ascii=False))
