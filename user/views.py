import json
from django.http import HttpResponse
from django.shortcuts import render
from T2S_Backend.decorators import get_required, post_required


def hello(request):
    a = {'a': 1, 'b': 2}
    b = json.dumps(a, ensure_ascii=False)
    return HttpResponse(b)


@ post_required
def logon(request):
    response = None
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















