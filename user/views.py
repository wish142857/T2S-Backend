import json

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
def login(request):
    response = None
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@ post_required
def logout(request):
    response = None
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@ post_required
def user_auth(request):
    response = None
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@ post_required
def change_password(request):
    response = None
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@ get_required
def get_info(request):
    response = None
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@ post_required
def update_info(request):
    response = None
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@ get_required
def get_info_plus(request):
    response = None
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@ post_required
def update_info_plus(request):
    response = None
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@ get_required
def get_info_picture(request):
    response = None
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@ post_required
def update_info_picture(request):
    response = None
    return HttpResponse(json.dumps(response, ensure_ascii=False))















