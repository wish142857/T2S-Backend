from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    name = request.GET.get("name")
    return HttpResponse('姓名：{}'.format(name))


