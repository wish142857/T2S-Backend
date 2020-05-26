import json

from django.contrib import auth
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from T2S_Backend.decorators import *
from T2S_Backend.globals import *
from T2S_Backend.utils import *
from user.models import Teacher, Student


def hello(request):
    a = {'a': 1, 'b': 2}
    b = json.dumps(a, ensure_ascii=False)
    return HttpResponse(b)


@ post_required
def logon(request):
    # *** 参数获取 ***
    _type = request.POST.get('type')
    _account = request.POST.get('account')
    _password = request.POST.get('password')
    _name = request.POST.get('name')
    # *** 合法性检测 ***
    if not check_none(_type, _account, _password, _name):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_empty(_account, _name) or not check_enum(_type, ('T', 'S')):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    # 创建用户账户
    try:
        user = User.objects.create_user(username=_account, password=_password)
    except IntegrityError:
        response = {'status': False, 'info': F_DUPLICATE_USERNAME}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # 创建关联教师/学生
    if _type == 'T':
        Teacher.objects.create(user=user, account=_account, password=_password, name=_name)
    else:
        Student.objects.create(user=user, account=_account, password=_password, name=_name)
    response = {'status': True, 'info': S_LOGON_SUCCEED}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@ post_required
@ logout_required
def login(request):
    # *** 参数获取 ***
    _type = request.POST.get('type')
    _account = request.POST.get('account')
    _password = request.POST.get('password')
    # *** 合法性检测 ***
    if not check_none(_type, _account, _password):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_empty(_account) or not check_enum(_type, ('T', 'S')):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    # 查找用户
    try:
        user = auth.authenticate(username=_account, password=_password)
        if user is None:
            raise User.DoesNotExist
        if _type == 'T':
            Teacher.objects.get(user=user)
        if _type == 'S':
            Student.objects.get(user=user)
    except (User.DoesNotExist, Teacher.DoesNotExist, Student.DoesNotExist):
        response = {'status': False, 'info': F_ERROR_USERNAME_OR_PASSWORD}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # 用户登录
    auth.login(request, user)
    response = {'status': True, 'info': S_LOGIN_SUCCEED}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@ post_required
@ login_required
def logout(request):
    # *** 请求处理 ***
    auth.logout(request)
    response = {'status': True, 'info': S_LOGOUT_SUCCEED}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@ post_required
@ login_required
def user_auth(request):
    # *** 参数获取 ***
    _type = request.POST.get('type')
    _teacher_number = request.POST.get('teacher_number')
    _student_number = request.POST.get('student_number')
    _id_number = request.POST.get('id_number')
    # *** 合法性检测 ***
    if not check_none(_type, _id_number):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if (not check_enum(_type, ('T', 'S'))) or (_type == 'T' and not check_none(_teacher_number)) or (_type == 'S' and not check_none(_student_number)):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    user = request.user
    if _type == 'T':
        try:
            teacher = Teacher.objects.get(user=user)
            if auth_teacher(_teacher_number, _id_number):
                teacher.auth_state = 'QD'
                teacher.save()
                response = {'status': True, 'info': S_AUTH_SUCCEED}
                return HttpResponse(json.dumps(response, ensure_ascii=False))
            else:
                response = {'status': False, 'info': F_AUTH_FAIL}
                return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Teacher.DoesNotExist:
            response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
    else:
        try:
            student = Student.objects.get(user=user)
            if auth_student(_student_number, _id_number):
                student.auth_state = 'QD'
                student.save()
                response = {'status': True, 'info': S_AUTH_SUCCEED}
                return HttpResponse(json.dumps(response, ensure_ascii=False))
            else:
                response = {'status': False, 'info': F_AUTH_FAIL}
                return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Student.DoesNotExist:
            response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
            return HttpResponse(json.dumps(response, ensure_ascii=False))


@ post_required
@ login_required
def change_password(request):
    # *** 参数获取 ***
    _old_password = request.POST.get('old_password')
    _new_password = request.POST.get('new_password')
    # *** 合法性检测 ***
    if not check_none(_old_password, _new_password):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_empty(_old_password, _new_password):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    user = request.user
    try:
        teacher = Teacher.objects.get(user=user)
        if user.check_password(_old_password):
            user.set_password(_new_password)
            user.save()
            teacher.password = _new_password
            teacher.save()
            response = {'status': True, 'info': S_CHANGE_PASSWORD_SUCCEED}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        else:
            response = {'status': False, 'info': F_ERROR_PASSWORD}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        if user.check_password(_old_password):
            user.set_password(_new_password)
            user.save()
            student.password = _new_password
            student.save()
            response = {'status': True, 'info': S_CHANGE_PASSWORD_SUCCEED}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        else:
            response = {'status': False, 'info': F_ERROR_PASSWORD}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Student.DoesNotExist:
        pass
    response = {'status': False, 'info': F_INTERNAL_ERROR}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


# TODO
@ get_required
def get_info(request):
    response = None
    return HttpResponse(json.dumps(response, ensure_ascii=False))

# TODO
@ post_required
def update_info(request):
    response = None
    return HttpResponse(json.dumps(response, ensure_ascii=False))

# TODO
@ get_required
def get_info_plus(request):
    response = None
    return HttpResponse(json.dumps(response, ensure_ascii=False))

# TODO
@ post_required
def update_info_plus(request):
    response = None
    return HttpResponse(json.dumps(response, ensure_ascii=False))

# TODO
@ get_required
def get_info_picture(request):
    response = None
    return HttpResponse(json.dumps(response, ensure_ascii=False))

# TODO
@ post_required
def update_info_picture(request):
    response = None
    return HttpResponse(json.dumps(response, ensure_ascii=False))

