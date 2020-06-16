import json
from T2S_Backend.decorators import *
from T2S_Backend.globals import *
from T2S_Backend.utils import *
from user.models import Teacher, Student


@get_required
@login_required
def recommend_fit_teacher(request):
    # *** 请求处理 ***
    user = request.user
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
                teacher_list.append((t.teacher_id, match_degree))
            teacher_list.sort(key=lambda e: e[1], reverse=True)
            response = {'status': True, 'info': S_RECOMMEND_SUCCEED, 'teacher_id_list': [e[0] for e in teacher_list[:N_RECOMMEND_MATCH_NUMBER]]}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Teacher.DoesNotExist:
            pass
        try:
            student = Student.objects.get(user=user)
            for t in teachers:
                match_degree = calculate_match_degree_s2t(student, t)
                teacher_list.append((t.teacher_id, match_degree))
            teacher_list.sort(key=lambda e: e[1], reverse=True)
            response = {'status': True, 'info': S_RECOMMEND_SUCCEED, 'teacher_id_list': [e[0] for e in teacher_list[:N_RECOMMEND_MATCH_NUMBER]]}
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
    user = request.user
    try:
        teachers = Teacher.objects.order_by('?')[:N_RECOMMEND_RANDOM_NUMBER]
        if teachers.count() <= 1:
            raise IndexError
        teacher_id = 0
        max_fans_count = -1
        try:
            teacher = Teacher.objects.get(user=user)
            for t in teachers:
                if t.teacher_id == teacher.teacher_id:
                    continue
                fans_count = t.user.teacher_fans.count() + t.user.student_fans.count()
                if fans_count > max_fans_count:
                    teacher_id = t.teacher_id
                    max_fans_count = fans_count
            response = {'status': True, 'info': S_RECOMMEND_SUCCEED, 'teacher_id': teacher_id, 'fans_count': max_fans_count}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Teacher.DoesNotExist:
            pass
        for t in teachers:
            fans_count = t.user.teacher_fans.count() + t.user.student_fans.count()
            if fans_count > max_fans_count:
                teacher_id = t.teacher_id
                max_fans_count = fans_count
        response = {'status': True, 'info': S_RECOMMEND_SUCCEED, 'teacher_id': teacher_id, 'fans_count': max_fans_count}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except IndexError:
        response = {'status': False, 'info': F_ERROR_NOT_FOUND}
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
@login_required
def recommend_random_teacher(request):
    # *** 请求处理 ***
    # *** 请求处理 ***
    user = request.user
    try:
        if Teacher.objects.count() <= 1:
            raise IndexError
        try:
            teacher = Teacher.objects.get(user=user)
            while True:
                teacher_id = Teacher.objects.order_by('?')[0].teacher_id
                if not teacher.teacher_id == teacher_id:
                    break
            response = {'status': True, 'info': S_RECOMMEND_SUCCEED, 'teacher_id': teacher_id}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Teacher.DoesNotExist:
            pass
        teacher_id = Teacher.objects.order_by('?')[0].teacher_id
        response = {'status': True, 'info': S_RECOMMEND_SUCCEED, 'teacher_id': teacher_id}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except IndexError:
        response = {'status': False, 'info': F_ERROR_NOT_FOUND}
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
@login_required
def recommend_fit_student(request):
    # *** 请求处理 ***
    user = request.user
    try:
        students = Student.objects.order_by('?')[:N_RECOMMEND_RANDOM_NUMBER]
        if students.count() <= 1:
            raise IndexError
        student_list = []
        try:
            teacher = Teacher.objects.get(user=user)
            for s in students:
                match_degree = calculate_match_degree_t2s(teacher, s)
                student_list.append((s.student_id, match_degree))
            student_list.sort(key=lambda e: e[1], reverse=True)
            response = {'status': True, 'info': S_RECOMMEND_SUCCEED, 'student_id_list': [e[0] for e in student_list[:N_RECOMMEND_MATCH_NUMBER]]}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Teacher.DoesNotExist:
            pass
        try:
            student = Student.objects.get(user=user)
            for s in students:
                if s.student_id == student.student_id:
                    continue
                match_degree = calculate_match_degree_s2s(student, s)
                student_list.append((s.student_id, match_degree))
            student_list.sort(key=lambda e: e[1], reverse=True)
            response = {'status': True, 'info': S_RECOMMEND_SUCCEED, 'student_id_list': [e[0] for e in student_list[:N_RECOMMEND_MATCH_NUMBER]]}
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
    user = request.user
    try:
        students = Student.objects.order_by('?')[:N_RECOMMEND_RANDOM_NUMBER]
        if students.count() <= 1:
            raise IndexError
        student_id = 0
        max_fans_count = -1
        try:
            student = Student.objects.get(user=user)
            for s in students:
                if s.student_id == student.student_id:
                    continue
                fans_count = s.user.teacher_fans.count() + s.user.student_fans.count()
                if fans_count > max_fans_count:
                    student_id = s.student_id
                    max_fans_count = fans_count
            response = {'status': True, 'info': S_RECOMMEND_SUCCEED, 'student_id': student_id, 'fans_count': max_fans_count}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Student.DoesNotExist:
            pass
        for s in students:
            fans_count = s.user.teacher_fans.count() + s.user.student_fans.count()
            if fans_count > max_fans_count:
                student_id = s.student_id
                max_fans_count = fans_count
        response = {'status': True, 'info': S_RECOMMEND_SUCCEED, 'student_id': student_id, 'fans_count': max_fans_count}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except IndexError:
        response = {'status': False, 'info': F_ERROR_NOT_FOUND}
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
@login_required
def recommend_random_student(request):
    # *** 请求处理 ***
    user = request.user
    try:
        if Student.objects.count() <= 1:
            raise IndexError
        try:
            student = Student.objects.get(user=user)
            while True:
                student_id = Student.objects.order_by('?')[0].student_id
                if not student.student_id == student_id:
                    break
            response = {'status': True, 'info': S_RECOMMEND_SUCCEED, 'student_id': student_id}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Student.DoesNotExist:
            pass
        student_id = Student.objects.order_by('?')[0].student_id
        response = {'status': True, 'info': S_RECOMMEND_SUCCEED, 'student_id': student_id}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except IndexError:
        response = {'status': False, 'info': F_ERROR_NOT_FOUND}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
