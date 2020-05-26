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
    user = auth.authenticate(username=_account, password=_password)
    if user is None:
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


# TODO
@ post_required
def user_auth(request):
    response = None
    return HttpResponse(json.dumps(response, ensure_ascii=False))

# TODO
@ post_required
def change_password(request):
    response = None
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

