import json
from django.shortcuts import render
from T2S_Backend.decorators import *
from T2S_Backend.globals import *
from T2S_Backend.utils import *
from user.models import Teacher, Student


@get_required
@login_required
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


@get_required
@login_required
def get_fanlist(request):
    # *** 请求处理 ***
    user = request.user
    fanlist_teacher = [t.teacher_id for t in user.teacher_fans.all()]
    fanlist_student = [s.student_id for s in user.student_fans.all()]
    response = {'status': True, 'info': S_QUERY_SUCCEED, 'fanlist_teacher': fanlist_teacher, 'fanlist_student': fanlist_student}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@post_required
@login_required
def add_to_watch(request):
    # *** 参数获取 ***
    _teacher_id = request.POST.get('teacher_id')
    _student_id = request.POST.get('student_id')
    # *** 合法性检测 ***
    if not check_optional(_teacher_id, _student_id):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    user = request.user
    try:
        teacher = Teacher.objects.get(user=user)
        if (_teacher_id is not None) and (not teacher.teacher_id.__eq__(_teacher_id)):
            try:
                u = Teacher.objects.get(teacher_id=_teacher_id).user
                teacher.follows.add(u)
            except Teacher.DoesNotExist:
                response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
                return HttpResponse(json.dumps(response, ensure_ascii=False))
        if _student_id is not None:
            try:
                u = Student.objects.get(student_id=_student_id).user
                teacher.follows.add(u)
            except Student.DoesNotExist:
                response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
                return HttpResponse(json.dumps(response, ensure_ascii=False))
        response = {'status': True, 'info': S_CREATE_SUCCEED}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        if _teacher_id is not None:
            try:
                u = Teacher.objects.get(teacher_id=_teacher_id).user
                student.follows.add(u)
            except Teacher.DoesNotExist:
                response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
                return HttpResponse(json.dumps(response, ensure_ascii=False))
        if (_student_id is not None) and (not student.student_id.__eq__(_student_id)):
            try:
                u = Student.objects.get(student_id=_student_id).user
                student.follows.add(u)
            except Student.DoesNotExist:
                response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
                return HttpResponse(json.dumps(response, ensure_ascii=False))
        response = {'status': True, 'info': S_CREATE_SUCCEED}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Student.DoesNotExist:
        pass
    response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@post_required
@login_required
def delete_from_watch(request):
    # *** 参数获取 ***
    _teacher_id = request.POST.get('teacher_id')
    _student_id = request.POST.get('student_id')
    # *** 合法性检测 ***
    if not check_optional(_teacher_id, _student_id):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    user = request.user
    try:
        teacher = Teacher.objects.get(user=user)
        if _teacher_id is not None:
            try:
                u = Teacher.objects.get(teacher_id=_teacher_id).user
                teacher.follows.remove(u)
            except Teacher.DoesNotExist:
                response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
                return HttpResponse(json.dumps(response, ensure_ascii=False))
        if _student_id is not None:
            try:
                u = Student.objects.get(student_id=_student_id).user
                teacher.follows.remove(u)
            except Student.DoesNotExist:
                response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
                return HttpResponse(json.dumps(response, ensure_ascii=False))
        response = {'status': True, 'info': S_DELETE_SUCCEED}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        if _teacher_id is not None:
            try:
                u = Teacher.objects.get(teacher_id=_teacher_id).user
                student.follows.remove(u)
            except Teacher.DoesNotExist:
                response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
                return HttpResponse(json.dumps(response, ensure_ascii=False))
        if _student_id is not None:
            try:
                u = Student.objects.get(student_id=_student_id).user
                student.follows.remove(u)
            except Student.DoesNotExist:
                response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
                return HttpResponse(json.dumps(response, ensure_ascii=False))
        response = {'status': True, 'info': S_DELETE_SUCCEED}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Student.DoesNotExist:
        pass
    response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
    return HttpResponse(json.dumps(response, ensure_ascii=False))
