import json

from django.contrib.auth.models import User

from T2S_Backend.decorators import *
from T2S_Backend.globals import *
from T2S_Backend.utils import *
from user.models import Teacher, Student


@get_required
@login_required
def recommend_fit_teacher(request):
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
    # 进行推荐
    try:
        teachers = Teacher.objects.order_by('?')[:N_RECOMMEND_RANDOM_NUMBER]
        if teachers.count() <= 1:
            raise IndexError
        teacher_list = []
        try:
            teacher = Teacher.objects.get(user=user)
            for t in teachers:
                if t.teacher_id == teacher.teacher_id:
                    continue
                match_degree = calculate_match_degree_t2t(teacher, t)
                teacher_list.append((t, match_degree))
            teacher_list.sort(key=lambda e: e[1], reverse=True)
            teacher_list = [e[0] for e in teacher_list[:N_RECOMMEND_MATCH_NUMBER]]
            teacher_info_list = []
            for t in teacher_list:
                teacher_info = {'teacher_id': t.teacher_id, 'name': t.name, 'gender': t.gender,
                                'school': t.school, 'department': t.department, 'auth_state': t.auth_state,
                                'fans_number': t.user.teacher_fans.count() + t.user.student_fans.count(), 'is_followed': False}
                try:
                    follow_list.get(username=t.user.username)
                    teacher_info['is_followed'] = True
                except User.DoesNotExist:
                    pass
                teacher_info_list.append(teacher_info)
            response = {'status': True, 'info': S_RECOMMEND_SUCCEED, 'teacher_info_list': teacher_info_list}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Teacher.DoesNotExist:
            pass
        try:
            student = Student.objects.get(user=user)
            for t in teachers:
                match_degree = calculate_match_degree_s2t(student, t)
                teacher_list.append((t, match_degree))
            teacher_list.sort(key=lambda e: e[1], reverse=True)
            teacher_list = [e[0] for e in teacher_list[:N_RECOMMEND_MATCH_NUMBER]]
            teacher_info_list = []
            for t in teacher_list:
                teacher_info = {'teacher_id': t.teacher_id, 'name': t.name, 'gender': t.gender,
                                'school': t.school, 'department': t.department, 'auth_state': t.auth_state,
                                'fans_number': t.user.teacher_fans.count() + t.user.student_fans.count(), 'is_followed': False}
                try:
                    follow_list.get(username=t.user.username)
                    teacher_info['is_followed'] = True
                except User.DoesNotExist:
                    pass
                teacher_info_list.append(teacher_info)
            response = {'status': True, 'info': S_RECOMMEND_SUCCEED, 'teacher_info_list': teacher_info_list}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Student.DoesNotExist:
            pass
        raise IndexError
    except IndexError:
        response = {'status': False, 'info': F_ERROR_NOT_FOUND}
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
@login_required
def recommend_hot_teacher(request):
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
    # 进行推荐
    try:
        teachers = Teacher.objects.order_by('?')[:N_RECOMMEND_RANDOM_NUMBER]
        if teachers.count() <= 1:
            raise IndexError
        hot_teacher = None
        max_fans_count = -1
        try:
            teacher = Teacher.objects.get(user=user)
            for t in teachers:
                if t.teacher_id == teacher.teacher_id:
                    continue
                fans_count = t.user.teacher_fans.count() + t.user.student_fans.count()
                if fans_count > max_fans_count:
                    hot_teacher = t
                    max_fans_count = fans_count
            if hot_teacher is None:
                response = {'status': False, 'info': F_ERROR_NOT_FOUND}
                return HttpResponse(json.dumps(response, ensure_ascii=False))
            teacher_info = {'teacher_id': hot_teacher.teacher_id, 'name': hot_teacher.name, 'gender': hot_teacher.gender,
                            'school': hot_teacher.school, 'department': hot_teacher.department, 'auth_state': hot_teacher.auth_state,
                            'fans_number': max_fans_count, 'is_followed': False}
            try:
                follow_list.get(username=hot_teacher.user.username)
                teacher_info['is_followed'] = True
            except User.DoesNotExist:
                pass
            response = {'status': True, 'info': S_RECOMMEND_SUCCEED, 'teacher_info': teacher_info}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Teacher.DoesNotExist:
            pass
        for t in teachers:
            fans_count = t.user.teacher_fans.count() + t.user.student_fans.count()
            if fans_count > max_fans_count:
                hot_teacher = t
                max_fans_count = fans_count
        if hot_teacher is None:
            response = {'status': False, 'info': F_ERROR_NOT_FOUND}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        teacher_info = {'teacher_id': hot_teacher.teacher_id, 'name': hot_teacher.name, 'gender': hot_teacher.gender,
                        'school': hot_teacher.school, 'department': hot_teacher.department, 'auth_state': hot_teacher.auth_state,
                        'fans_number': max_fans_count, 'is_followed': False}
        try:
            follow_list.get(username=hot_teacher.user.username)
            teacher_info['is_followed'] = True
        except User.DoesNotExist:
            pass
        response = {'status': True, 'info': S_RECOMMEND_SUCCEED, 'teacher_info': teacher_info}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except IndexError:
        response = {'status': False, 'info': F_ERROR_NOT_FOUND}
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
@login_required
def recommend_random_teacher(request):
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
    # 进行推荐
    try:
        if Teacher.objects.count() <= 1:
            raise IndexError
        try:
            teacher = Teacher.objects.get(user=user)
            while True:
                random_teacher = Teacher.objects.order_by('?')[0]
                if not teacher.teacher_id == random_teacher.teacher_id:
                    break
            if random_teacher is None:
                response = {'status': False, 'info': F_ERROR_NOT_FOUND}
                return HttpResponse(json.dumps(response, ensure_ascii=False))
            teacher_info = {'teacher_id': random_teacher.teacher_id, 'name': random_teacher.name, 'gender': random_teacher.gender,
                            'school': random_teacher.school, 'department': random_teacher.department, 'auth_state': random_teacher.auth_state,
                            'fans_number': random_teacher.user.teacher_fans.count() + random_teacher.user.student_fans.count(), 'is_followed': False}
            try:
                follow_list.get(username=random_teacher.user.username)
                teacher_info['is_followed'] = True
            except User.DoesNotExist:
                pass
            response = {'status': True, 'info': S_RECOMMEND_SUCCEED, 'teacher_info': teacher_info}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Teacher.DoesNotExist:
            pass
        random_teacher = Teacher.objects.order_by('?')[0]
        if random_teacher is None:
            response = {'status': False, 'info': F_ERROR_NOT_FOUND}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        teacher_info = {'teacher_id': random_teacher.teacher_id, 'name': random_teacher.name, 'gender': random_teacher.gender,
                        'school': random_teacher.school, 'department': random_teacher.department, 'auth_state': random_teacher.auth_state,
                        'fans_number': random_teacher.user.teacher_fans.count() + random_teacher.user.student_fans.count(), 'is_followed': False}
        try:
            follow_list.get(username=random_teacher.user.username)
            teacher_info['is_followed'] = True
        except User.DoesNotExist:
            pass
        response = {'status': True, 'info': S_RECOMMEND_SUCCEED, 'teacher_info': teacher_info}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except IndexError:
        response = {'status': False, 'info': F_ERROR_NOT_FOUND}
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
@login_required
def recommend_fit_student(request):
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
    # 进行推荐
    try:
        students = Student.objects.order_by('?')[:N_RECOMMEND_RANDOM_NUMBER]
        if students.count() <= 1:
            raise IndexError
        student_list = []
        try:
            teacher = Teacher.objects.get(user=user)
            for s in students:
                match_degree = calculate_match_degree_t2s(teacher, s)
                student_list.append((s, match_degree))
            student_list.sort(key=lambda e: e[1], reverse=True)
            student_list = [e[0] for e in student_list[:N_RECOMMEND_MATCH_NUMBER]]
            student_info_list = []
            for s in student_list:
                student_info = {'student_id': s.student_id, 'name': s.name, 'gender': s.gender,
                                'school': s.school, 'department': s.department, 'auth_state': s.auth_state,
                                'fans_number': s.user.teacher_fans.count() + s.user.student_fans.count(), 'is_followed': False}
                try:
                    follow_list.get(username=s.user.username)
                    student_info['is_followed'] = True
                except User.DoesNotExist:
                    pass
                student_info_list.append(student_info)
            response = {'status': True, 'info': S_RECOMMEND_SUCCEED, 'student_info_list': student_info_list}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Teacher.DoesNotExist:
            pass
        try:
            student = Student.objects.get(user=user)
            for s in students:
                if s.student_id == student.student_id:
                    continue
                match_degree = calculate_match_degree_s2s(student, s)
                student_list.append((s, match_degree))
            student_list.sort(key=lambda e: e[1], reverse=True)
            student_list = [e[0] for e in student_list[:N_RECOMMEND_MATCH_NUMBER]]
            student_info_list = []
            for s in student_list:
                student_info = {'student_id': s.student_id, 'name': s.name, 'gender': s.gender,
                                'school': s.school, 'department': s.department, 'auth_state': s.auth_state,
                                'fans_number': s.user.teacher_fans.count() + s.user.student_fans.count(), 'is_followed': False}
                try:
                    follow_list.get(username=s.user.username)
                    student_info['is_followed'] = True
                except User.DoesNotExist:
                    pass
                student_info_list.append(student_info)
            response = {'status': True, 'info': S_RECOMMEND_SUCCEED, 'student_info_list': student_info_list}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Student.DoesNotExist:
            pass
        raise IndexError
    except IndexError:
        response = {'status': False, 'info': F_ERROR_NOT_FOUND}
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
@login_required
def recommend_hot_student(request):
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
    # 进行推荐
    try:
        students = Student.objects.order_by('?')[:N_RECOMMEND_RANDOM_NUMBER]
        if students.count() <= 1:
            raise IndexError
        hot_student = None
        max_fans_count = -1
        try:
            student = Student.objects.get(user=user)
            for s in students:
                if s.student_id == student.student_id:
                    continue
                fans_count = s.user.teacher_fans.count() + s.user.student_fans.count()
                if fans_count > max_fans_count:
                    hot_student = s
                    max_fans_count = fans_count
            if hot_student is None:
                response = {'status': False, 'info': F_ERROR_NOT_FOUND}
                return HttpResponse(json.dumps(response, ensure_ascii=False))
            student_info = {'student_id': hot_student.student_id, 'name': hot_student.name, 'gender': hot_student.gender,
                            'school': hot_student.school, 'department': hot_student.department, 'auth_state': hot_student.auth_state,
                            'fans_number': max_fans_count, 'is_followed': False}
            try:
                follow_list.get(username=hot_student.user.username)
                student_info['is_followed'] = True
            except User.DoesNotExist:
                pass
            response = {'status': True, 'info': S_RECOMMEND_SUCCEED, 'student_info': student_info}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Student.DoesNotExist:
            pass
        for s in students:
            fans_count = s.user.teacher_fans.count() + s.user.student_fans.count()
            if fans_count > max_fans_count:
                hot_student = s
                max_fans_count = fans_count
        if hot_student is None:
            response = {'status': False, 'info': F_ERROR_NOT_FOUND}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        student_info = {'student_id': hot_student.student_id, 'name': hot_student.name, 'gender': hot_student.gender,
                        'school': hot_student.school, 'department': hot_student.department, 'auth_state': hot_student.auth_state,
                        'fans_number': max_fans_count, 'is_followed': False}
        try:
            follow_list.get(username=hot_student.user.username)
            student_info['is_followed'] = True
        except User.DoesNotExist:
            pass
        response = {'status': True, 'info': S_RECOMMEND_SUCCEED, 'student_info': student_info}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except IndexError:
        response = {'status': False, 'info': F_ERROR_NOT_FOUND}
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
@login_required
def recommend_random_student(request):
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
    # 进行推荐
    try:
        if Student.objects.count() <= 1:
            raise IndexError
        try:
            student = Student.objects.get(user=user)
            while True:
                random_student = Student.objects.order_by('?')[0]
                if not student.student_id == random_student.student_id:
                    break
            if random_student is None:
                response = {'status': False, 'info': F_ERROR_NOT_FOUND}
                return HttpResponse(json.dumps(response, ensure_ascii=False))
            student_info = {'student_id': random_student.student_id, 'name': random_student.name, 'gender': random_student.gender,
                            'school': random_student.school, 'department': random_student.department, 'auth_state': random_student.auth_state,
                            'fans_number': random_student.user.teacher_fans.count() + random_student.user.student_fans.count(), 'is_followed': False}
            try:
                follow_list.get(username=random_student.user.username)
                student_info['is_followed'] = True
            except User.DoesNotExist:
                pass
            response = {'status': True, 'info': S_RECOMMEND_SUCCEED, 'student_info': student_info}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Student.DoesNotExist:
            pass
        random_student = Student.objects.order_by('?')[0]
        if random_student is None:
            response = {'status': False, 'info': F_ERROR_NOT_FOUND}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        student_info = {'student_id': random_student.student_id, 'name': random_student.name, 'gender': random_student.gender,
                        'school': random_student.school, 'department': random_student.department, 'auth_state': random_student.auth_state,
                        'fans_number': random_student.user.teacher_fans.count() + random_student.user.student_fans.count(), 'is_followed': False}
        try:
            follow_list.get(username=random_student.user.username)
            student_info['is_followed'] = True
        except User.DoesNotExist:
            pass
        response = {'status': True, 'info': S_RECOMMEND_SUCCEED, 'student_info': student_info}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except IndexError:
        response = {'status': False, 'info': F_ERROR_NOT_FOUND}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
