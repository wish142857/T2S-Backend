import json
from django.shortcuts import render
from T2S_Backend.decorators import *
from T2S_Backend.globals import *
from T2S_Backend.utils import *
from user.models import Teacher, Student


@ get_required
@ login_required
def get_watchlist(request):
    # *** 请求处理 ***
    user = request.user
    watchlist_teacher = []
    watchlist_student = []
    try:
        teacher = Teacher.objects.get(user=user)
        for u in teacher.follows.all():
            try:
                t = Teacher.objects.get(user=u)
                watchlist_teacher.append(t.teacher_id)
                continue
            except Teacher.DoesNotExist:
                pass
            try:
                s = Student.objects.get(user=u)
                watchlist_student.append(s.student_id)
                continue
            except Student.DoesNotExist:
                pass
        response = {'status': True, 'info': S_QUERY_SUCCEED, 'watchlist_teacher': watchlist_teacher, 'watchlist_student': watchlist_student}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        for u in student.follows.all():
            try:
                t = Teacher.objects.get(user=u)
                watchlist_teacher.append(t.teacher_id)
                continue
            except Teacher.DoesNotExist:
                pass
            try:
                s = Student.objects.get(user=u)
                watchlist_student.append(s.student_id)
                continue
            except Student.DoesNotExist:
                pass
        response = {'status': True, 'info': S_QUERY_SUCCEED, 'watchlist_teacher': watchlist_teacher, 'watchlist_student': watchlist_student}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Student.DoesNotExist:
        pass
    response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@ get_required
@ login_required
def get_fanlist(request):
    # *** 请求处理 ***
    user = request.user
    fanlist_teacher = [t.teacher_id for t in user.teacher_fans.all()]
    fanlist_student = [s.student_id for s in user.student_fans.all()]
    response = {'status': True, 'info': S_QUERY_SUCCEED, 'fanlist_teacher': fanlist_teacher, 'fanlist_student': fanlist_student}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@ post_required
@ login_required
def add_to_watch(request):
    # TODO
    pass


@ post_required
@ login_required
def delete_from_watch(request):
    # TODO
    pass
