import json
from collections import Counter

from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone

from T2S_Backend.decorators import *
from T2S_Backend.globals import *
from T2S_Backend.utils import *
from search.models import SearchRecord
from user.models import Teacher, Student
from intention.models import Recruitment, Application


@get_required
@login_required
def get_search_record(request):
    # *** 参数获取 ***
    try:
        _number = int(request.GET.get('number'))
    except (TypeError, ValueError):
        _number = 0
    if _number is None or _number <= 0:
        _number = N_DEFAULT_GET_SEARCH_RECORD_NUMBER
    # *** 请求处理 ***
    user = request.user
    search_record_list = [sr.search_key for sr in user.searchrecord_set.all().order_by('-search_time')[:_number]]
    response = {'status': True, 'info': S_QUERY_SUCCEED, 'search_record_list': search_record_list}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
def get_hot_search_record(request):
    # *** 参数获取 ***
    try:
        _number = int(request.GET.get('number'))
    except (TypeError, ValueError):
        _number = 0
    if _number is None or _number <= 0:
        _number = N_DEFAULT_GET_HOT_SEARCH_RECORD_NUMBER
    # *** 请求处理 ***
    search_record_counter = Counter([sr.search_key for sr in SearchRecord.objects.all()])
    search_record_list = [sr[0] for sr in search_record_counter.most_common(_number)]
    response = {'status': True, 'info': S_QUERY_SUCCEED, 'search_record_list': search_record_list}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@post_required
@login_required
def delete_search_record(request):
    # *** 参数获取 ***
    _key = request.POST.get('key')
    # *** 合法性检测 ***
    if not check_necessary(_key):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_nonempty(_key):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    user = request.user
    try:
        SearchRecord.objects.get(owner_user=user, search_key=_key).delete()
        response = {'status': True, 'info': S_DELETE_SUCCEED}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except SearchRecord.DoesNotExist:
        response = {'status': False, 'info': F_DELETE_FAIL}
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
@login_required
def search_teacher(request):
    # *** 参数获取 ***
    _key = request.GET.get('key')
    # *** 合法性检测 ***
    if not check_necessary(_key):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_nonempty(_key):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    # 获取用户关注列表
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
    # 进行关键字搜索
    keys = _key.split()
    for key in keys:
        try:
            search_record = SearchRecord.objects.get(owner_user=user, search_key=key)
            search_record.search_time = timezone.now()
            search_record.save()
        except SearchRecord.DoesNotExist:
            SearchRecord.objects.create(owner_user=user, search_key=key, search_time=timezone.now())
    teachers = Teacher.objects.filter(
        Q(account__icontains=keys[0]) | Q(name__icontains=keys[0]) |
        Q(school__icontains=keys[0]) | Q(department__icontains=keys[0]) |
        Q(introduction__icontains=keys[0]) | Q(research_fields__icontains=keys[0])
    )
    for key in keys[1:]:
        teachers = teachers | Teacher.objects.filter(
            Q(account__icontains=key) | Q(name__icontains=key) |
            Q(school__icontains=key) | Q(department__icontains=key) |
            Q(introduction__icontains=key) | Q(research_fields__icontains=key)
        )
    if teachers.all().count() == 0:
        response = {'status': False, 'info': F_ERROR_NOT_FOUND}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    try:
        teacher = Teacher.objects.get(user=user)
        teacher_info_list = []
        for t in teachers.all():
            teacher_info = {'teacher_id': t.teacher_id, 'name': t.name, 'gender': t.gender, 'school': t.school, 'department': t.department,
                            'auth_state': t.auth_state, 'fans_number': t.user.teacher_fans.count() + t.user.student_fans.count(),
                            'is_followed': False, 'match_degree': calculate_match_degree_t2t(teacher, t)}
            try:
                follow_list.get(username=t.user.username)
                teacher_info['is_followed'] = True
            except User.DoesNotExist:
                pass
            teacher_info_list.append(teacher_info)
        response = {'status': True, 'info': S_SEARCH_SUCCEED, 'teacher_info_list': teacher_info_list}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        teacher_info_list = []
        for t in teachers.all():
            teacher_info = {'teacher_id': t.teacher_id, 'name': t.name, 'gender': t.gender, 'school': t.school,
                            'department': t.department, 'auth_state': t.auth_state, 'fans_number': t.user.teacher_fans.count() + t.user.student_fans.count(),
                            'is_followed': False, 'match_degree': calculate_match_degree_s2t(student, t)}
            try:
                follow_list.get(username=t.user.username)
                teacher_info['is_followed'] = True
            except User.DoesNotExist:
                pass
            teacher_info_list.append(teacher_info)
        response = {'status': True, 'info': S_SEARCH_SUCCEED, 'teacher_info_list': teacher_info_list}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Student.DoesNotExist:
        pass
    response = {'status': False, 'info': F_ERROR_NOT_FOUND}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
@login_required
def search_student(request):
    # *** 参数获取 ***
    _key = request.GET.get('key')
    # *** 合法性检测 ***
    if not check_necessary(_key):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_nonempty(_key):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    # 获取用户关注列表
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
    # 进行关键字搜索
    keys = _key.split()
    for key in keys:
        try:
            search_record = SearchRecord.objects.get(owner_user=user, search_key=key)
            search_record.search_time = timezone.now()
            search_record.save()
        except SearchRecord.DoesNotExist:
            SearchRecord.objects.create(owner_user=user, search_key=key, search_time=timezone.now())
    students = Student.objects.filter(
        Q(account__icontains=keys[0]) | Q(name__icontains=keys[0]) |
        Q(school__icontains=keys[0]) | Q(department__icontains=keys[0]) | Q(major__icontains=keys[0]) |
        Q(introduction__icontains=keys[0]) | Q(research_experience__icontains=keys[0])
    )
    for key in keys[1:]:
        students = students | Student.objects.filter(
            Q(account__icontains=key) | Q(name__icontains=key) |
            Q(school__icontains=key) | Q(department__icontains=key) | Q(major__icontains=key) |
            Q(introduction__icontains=key) | Q(research_experience__icontains=key)
        )
    if students.all().count() == 0:
        response = {'status': False, 'info': F_ERROR_NOT_FOUND}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    try:
        teacher = Teacher.objects.get(user=user)
        student_info_list = []
        for s in students.all():
            student_info = {'student_id': s.student_id, 'name': s.name, 'gender': s.gender, 'school': s.school,
                            'department': s.department, 'auth_state': s.auth_state, 'fans_number': s.user.teacher_fans.count() + s.user.student_fans.count(),
                            'is_followed': False, 'match_degree': calculate_match_degree_t2s(teacher, s)}
            try:
                follow_list.get(username=s.user.username)
                student_info['is_followed'] = True
            except User.DoesNotExist:
                pass
            student_info_list.append(student_info)
        response = {'status': True, 'info': S_SEARCH_SUCCEED, 'student_info_list': student_info_list}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        student_info_list = []
        for s in students.all():
            student_info = {'student_id': s.student_id, 'name': s.name, 'gender': s.gender, 'school': s.school,
                            'department': s.department, 'auth_state': s.auth_state, 'fans_number': s.user.teacher_fans.count() + s.user.student_fans.count(),
                            'is_followed': False, 'match_degree': calculate_match_degree_s2s(student, s)}
            try:
                follow_list.get(username=s.user.username)
                student_info['is_followed'] = True
            except User.DoesNotExist:
                pass
            student_info_list.append(student_info)
        response = {'status': True, 'info': S_SEARCH_SUCCEED, 'student_info_list': student_info_list}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Student.DoesNotExist:
        pass
    response = {'status': False, 'info': F_ERROR_NOT_FOUND}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
@login_required
def search_recruit_intention(request):
    # *** 参数获取 ***
    _key = request.GET.get('key')
    # *** 合法性检测 ***
    if not check_necessary(_key):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_nonempty(_key):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    user = request.user
    keys = _key.split()
    for key in keys:
        try:
            search_record = SearchRecord.objects.get(owner_user=user, search_key=key)
            search_record.search_time = timezone.now()
            search_record.save()
        except SearchRecord.DoesNotExist:
            SearchRecord.objects.create(owner_user=user, search_key=key, search_time=timezone.now())
    recruitments = Recruitment.objects.filter(
        Q(research_fields__icontains=keys[0]) | Q(introduction__icontains=keys[0])
    )
    for key in keys[1:]:
        recruitments = recruitments | Recruitment.objects.filter(
            Q(research_fields__icontains=key) | Q(introduction__icontains=key)
        )
    if recruitments.all().count() == 0:
        response = {'status': False, 'info': F_ERROR_NOT_FOUND}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    try:
        teacher = Teacher.objects.get(user=user)
        follow_list = teacher.follows
        recruitment_info_list = []
        for r in recruitments.all():
            recruitment_info = {'recruitment_id': r.recruitment_id, 'teacher_id': r.publisher.teacher_id, 'teacher_name': r.publisher.name,
                                'teacher_school': r.publisher.school, 'teacher_department': r.publisher.department, 'auth_state': r.publisher.auth_state,
                                'fans_number': r.publisher.user.teacher_fans.count() + r.publisher.user.student_fans.count(), 'is_followed': False,
                                'recruitment_type': r.recruitment_type, 'recruitment_number': r. recruitment_number, 'research_fields': r.research_fields,
                                'intention_state': r.intention_state, 'match_degree': calculate_match_degree_t2r(teacher, r)}
            try:
                follow_list.get(username=r.publisher.user.username)
                recruitment_info['is_followed'] = True
            except User.DoesNotExist:
                pass
            recruitment_info_list.append(recruitment_info)
        response = {'status': True, 'info': S_SEARCH_SUCCEED, 'recruitment_info_list': recruitment_info_list}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        follow_list = student.follows
        recruitment_info_list = []
        for r in recruitments.all():
            recruitment_info = {'recruitment_id': r.recruitment_id, 'teacher_id': r.publisher.teacher_id, 'teacher_name': r.publisher.name,
                                'teacher_school': r.publisher.school, 'teacher_department': r.publisher.department, 'auth_state': r.publisher.auth_state,
                                'fans_number': r.publisher.user.teacher_fans.count() + r.publisher.user.student_fans.count(), 'is_followed': False,
                                'recruitment_type': r.recruitment_type, 'recruitment_number': r.recruitment_number, 'research_fields': r.research_fields,
                                'intention_state': r.intention_state, 'match_degree': calculate_match_degree_s2r(student, r)}
            try:
                follow_list.get(username=r.publisher.user.username)
                recruitment_info['is_followed'] = True
            except User.DoesNotExist:
                pass
            recruitment_info_list.append(recruitment_info)
        response = {'status': True, 'info': S_SEARCH_SUCCEED, 'recruitment_info_list': recruitment_info_list}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Student.DoesNotExist:
        pass
    response = {'status': False, 'info': F_ERROR_NOT_FOUND}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
@login_required
def search_apply_intention(request):
    # *** 参数获取 ***
    _key = request.GET.get('key')
    # *** 合法性检测 ***
    if not check_necessary(_key):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_nonempty(_key):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    user = request.user
    keys = _key.split()
    for key in keys:
        try:
            search_record = SearchRecord.objects.get(owner_user=user, search_key=key)
            search_record.search_time = timezone.now()
            search_record.save()
        except SearchRecord.DoesNotExist:
            SearchRecord.objects.create(owner_user=user, search_key=key, search_time=timezone.now())
    applications = Application.objects.filter(
        Q(research_interests__icontains=keys[0]) | Q(introduction__icontains=keys[0])
    )
    for key in keys:
        applications = applications | Application.objects.filter(
            Q(research_interests__icontains=key) | Q(introduction__icontains=key)
        )
    if applications.all().count() == 0:
        response = {'status': False, 'info': F_ERROR_NOT_FOUND}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    try:
        teacher = Teacher.objects.get(user=user)
        follow_list = teacher.follows
        application_info_list = []
        for a in applications.all():
            application_info = {'application_id': a.application_id, 'student_id': a.publisher.student_id, 'student_name': a.publisher.name,
                                'student_school': a.publisher.school, 'student_department': a.publisher.department, 'auth_state': a.publisher.auth_state,
                                'fans_number': a.publisher.user.teacher_fans.count() + a.publisher.user.student_fans.count(), 'is_followed': False,
                                'research_interests': a.research_interests, 'intention_state': a. intention_state, 'match_degree': calculate_match_degree_t2a(teacher, a)}
            try:
                follow_list.get(username=a.publisher.user.username)
                application_info['is_followed'] = True
            except User.DoesNotExist:
                pass
            application_info_list.append(application_info)
        response = {'status': True, 'info': S_SEARCH_SUCCEED, 'application_info_list': application_info_list}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        follow_list = student.follows
        application_info_list = []
        for a in applications.all():
            application_info = {'application_id': a.application_id, 'student_id': a.publisher.student_id, 'student_name': a.publisher.name,
                                'student_school': a.publisher.school, 'student_department': a.publisher.department, 'auth_state': a.publisher.auth_state,
                                'fans_number': a.publisher.user.teacher_fans.count() + a.publisher.user.student_fans.count(), 'is_followed': False,
                                'research_interests': a.research_interests, 'intention_state': a. intention_state, 'match_degree': calculate_match_degree_s2a(student, a)}
            try:
                follow_list.get(username=a.publisher.user.username)
                application_info['is_followed'] = True
            except User.DoesNotExist:
                pass
            application_info_list.append(application_info)
        response = {'status': True, 'info': S_SEARCH_SUCCEED, 'application_info_list': application_info_list}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Student.DoesNotExist:
        pass
    response = {'status': False, 'info': F_ERROR_NOT_FOUND}
    return HttpResponse(json.dumps(response, ensure_ascii=False))
