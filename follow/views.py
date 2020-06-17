import json

from django.contrib.auth.models import User
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
    follow_list = None
    try:
        follow_list = Teacher.objects.get(user=user).follows
    except Teacher.DoesNotExist:
        pass
    try:
        follow_list = Student.objects.get(user=user).follows
    except Student.DoesNotExist:
        pass
    if follow_list is None:
        response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    watchlist_teachers = []
    watchlist_students = []
    for u in follow_list.all():
        try:
            t = Teacher.objects.get(user=u)
            t_info = {'teacher_id': t.teacher_id, 'name': t.name, 'gender': t.gender,
                      'school': t.school, 'department': t.department, 'auth_state': t.auth_state,
                      'fans_number': t.user.teacher_fans.count() + t.user.student_fans.count(), 'is_followed': True}
            watchlist_teachers.append(t_info)
            continue
        except Teacher.DoesNotExist:
            pass
        try:
            s = Student.objects.get(user=u)
            s_info = {'student_id': s.student_id, 'name': s.name, 'gender': s.gender,
                      'school': s.school, 'department': s.department, 'auth_state': s.auth_state,
                      'fans_number': s.user.teacher_fans.count() + s.user.student_fans.count(), 'is_followed': True}
            watchlist_students.append(s_info)
            continue
        except Student.DoesNotExist:
            pass
    response = {'status': True, 'info': S_QUERY_SUCCEED, 'watchlist_teachers': watchlist_teachers, 'watchlist_students': watchlist_students}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
@login_required
def get_fanlist(request):
    # *** 请求处理 ***
    user = request.user
    follow_list = None
    try:
        follow_list = Teacher.objects.get(user=user).follows
    except Teacher.DoesNotExist:
        pass
    try:
        follow_list = Student.objects.get(user=user).follows
    except Student.DoesNotExist:
        pass
    if follow_list is None:
        response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    fanlist_teachers = []
    fanlist_students = []
    for t in user.teacher_fans.all():
        t_info = {'teacher_id': t.teacher_id, 'name': t.name, 'gender': t.gender,
                  'school': t.school, 'department': t.department, 'auth_state': t.auth_state,
                  'fans_number': t.user.teacher_fans.count() + t.user.student_fans.count(), 'is_followed': False}
        try:
            follow_list.get(username=t.user.username)
            t_info['is_followed'] = True
        except User.DoesNotExist:
            pass
        fanlist_teachers.append(t_info)
    for s in user.student_fans.all():
        s_info = {'student_id': s.student_id, 'name': s.name, 'gender': s.gender,
                  'school': s.school, 'department': s.department, 'auth_state': s.auth_state,
                  'fans_number': s.user.teacher_fans.count() + s.user.student_fans.count(), 'is_followed': False}
        try:
            follow_list.get(username=s.user.username)
            s_info['is_followed'] = True
        except User.DoesNotExist:
            pass
        fanlist_students.append(s_info)
    response = {'status': True, 'info': S_QUERY_SUCCEED, 'fanlist_teachers': fanlist_teachers, 'fanlist_students': fanlist_students}
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
        if (_teacher_id is not None) and (str(teacher.teacher_id) != _teacher_id):
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
        if (_student_id is not None) and (str(student.student_id) != _student_id):
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
