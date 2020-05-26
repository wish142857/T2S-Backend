"""
装饰器
"""
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse


# [decorator] GET请求限定
def get_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.method == 'GET':
            return HttpResponse(status=403)
        return func(request, *args, **kwargs)
    return wrapper


# [decorator] POST请求限定
def post_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.method == 'POST':
            return HttpResponse(status=403)
        return func(request, *args, **kwargs)
    return wrapper


# [decorator] 已登录限定
def login_required(func):
    def wrapper(request, *args, **kwargs):
        # 登录状态检测
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=401)
        return func(request, *args, **kwargs)
    return wrapper


# [decorator] 未登录限定
def logout_required(func):
    def wrapper(request, *args, **kwargs):
        # 登录状态检测
        user = request.user
        if user.is_authenticated:
            return HttpResponse(status=403)
        return func(request, *args, **kwargs)
    return wrapper


# [decorator] 超级用户限定
def superuser_required(func):
    def wrapper(request, *args, **kwargs):
        # 登录状态检测 / 权限状态检测
        user = request.user
        if not user.is_authenticated or not user.is_superuser:
            return HttpResponse(status=401)
        return func(request, *args, **kwargs)
    return wrapper
