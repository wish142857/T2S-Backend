import datetime
import json
from io import StringIO
from PIL import Image

from django.contrib import auth
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse
from T2S_Backend.decorators import *
from T2S_Backend.globals import *
from T2S_Backend.utils import *
from information.models import Information
from user.models import Teacher, Student


@post_required
def logon(request):
    # *** 参数获取 ***
    _type = request.POST.get('type')
    _account = request.POST.get('account')
    _password = request.POST.get('password')
    _name = request.POST.get('name')
    # *** 合法性检测 ***
    if not check_necessary(_type, _account, _password, _name):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_nonempty(_account, _name) or not check_enumeration(_type, ('T', 'S')):
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
        teacher = Teacher.objects.create(user=user, account=_account, password=_password, name=_name)
        Information.objects.create(
            receiver_teacher=teacher,
            receiver_type='T',
            information_type='T',
            information_state='N',
            information_content=bytes(I_NEW_LOGIN % _account, encoding="utf8"),
        )
    else:
        student = Student.objects.create(user=user, account=_account, password=_password, name=_name)
        Information.objects.create(
            receiver_student=student,
            receiver_type='S',
            information_type='T',
            information_state='N',
            information_content=bytes(I_NEW_LOGIN % _account, encoding="utf8"),
        )
    response = {'status': True, 'info': S_LOGON_SUCCEED}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@post_required
def login(request):
    # *** 参数获取 ***
    _type = request.POST.get('type')
    _account = request.POST.get('account')
    _password = request.POST.get('password')
    # *** 合法性检测 ***
    if not check_necessary(_type, _account, _password):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_nonempty(_account) or not check_enumeration(_type, ('T', 'S')):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    # 用户注销
    if request.user.is_authenticated:
        auth.logout(request)
    # 用户查找
    try:
        user = auth.authenticate(username=_account, password=_password)
        if user is None:
            raise User.DoesNotExist
        if _type == 'T':
            Teacher.objects.get(user=user)
        if _type == 'S':
            Student.objects.get(user=user)
    except (User.DoesNotExist, Teacher.DoesNotExist, Student.DoesNotExist):
        response = {'status': False, 'info': F_ERROR_USERNAME_OR_PASSWORD}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # 用户登录
    auth.login(request, user)
    response = {'status': True, 'info': S_LOGIN_SUCCEED}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@post_required
@login_required
def logout(request):
    # *** 请求处理 ***
    auth.logout(request)
    response = {'status': True, 'info': S_LOGOUT_SUCCEED}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@post_required
@login_required
def user_auth(request):
    # *** 参数获取 ***
    _teacher_number = request.POST.get('teacher_number')
    _student_number = request.POST.get('student_number')
    _id_number = request.POST.get('id_number')
    # *** 合法性检测 ***
    if not check_necessary(_id_number) or not check_optional(_teacher_number, _student_number):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    user = request.user
    try:
        teacher = Teacher.objects.get(user=user)
        if auth_teacher(_teacher_number, _id_number):
            teacher.auth_state = 'QD'
            teacher.teacher_number = _teacher_number
            teacher.id_number = _id_number
            teacher.save()
            response = {'status': True, 'info': S_AUTH_SUCCEED}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        else:
            response = {'status': False, 'info': F_AUTH_FAIL}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        if auth_student(_student_number, _id_number):
            student.auth_state = 'QD'
            student.student_number = _student_number
            student.id_number = _id_number
            student.save()
            response = {'status': True, 'info': S_AUTH_SUCCEED}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        else:
            response = {'status': False, 'info': F_AUTH_FAIL}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Student.DoesNotExist:
        pass
    response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@post_required
@login_required
def change_password(request):
    # *** 参数获取 ***
    _old_password = request.POST.get('old_password')
    _new_password = request.POST.get('new_password')
    # *** 合法性检测 ***
    if not check_necessary(_old_password, _new_password):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    user = request.user
    try:
        teacher = Teacher.objects.get(user=user)
        if user.check_password(_old_password):
            user.set_password(_new_password)
            user.save()
            teacher.password = _new_password
            teacher.save()
            Information.objects.create(
                receiver_teacher=teacher,
                receiver_type='T',
                information_type='T',
                information_state='N',
                information_content=bytes(I_NEW_PASSWORD % (teacher.name, teacher.account), encoding="utf8"),
            )
            response = {'status': True, 'info': S_CHANGE_PASSWORD_SUCCEED}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        else:
            response = {'status': False, 'info': F_ERROR_PASSWORD}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        if user.check_password(_old_password):
            user.set_password(_new_password)
            user.save()
            student.password = _new_password
            student.save()
            Information.objects.create(
                receiver_student=student,
                receiver_type='S',
                information_type='T',
                information_state='N',
                information_content=bytes(I_NEW_PASSWORD % (student.name, student.account), encoding="utf8"),
            )
            response = {'status': True, 'info': S_CHANGE_PASSWORD_SUCCEED}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        else:
            response = {'status': False, 'info': F_ERROR_PASSWORD}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Student.DoesNotExist:
        pass
    response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
def get_info(request):
    # *** 参数获取 ***
    _type = request.GET.get('type')
    _teacher_id = request.GET.get('teacher_id')
    _student_id = request.GET.get('student_id')
    # *** 合法性检测 ***
    if not check_necessary(_type):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_enumeration(_type, ('T', 'S', 'I')):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if (_type == 'T' and _teacher_id is None) or (_type == 'S' and _student_id is None):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    if _type == 'T':
        try:
            teacher = Teacher.objects.get(teacher_id=_teacher_id)
            response = {
                'status': True,
                'info': S_QUERY_SUCCEED,
                'teacher_id': teacher.teacher_id,
                'account': teacher.account,
                'name': teacher.name,
                'gender': teacher.gender,
                'school': teacher.school,
                'department': teacher.department,
                'title': teacher.title,
                'auth_state': teacher.auth_state,
            }
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Teacher.DoesNotExist:
            response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
    elif _type == 'S':
        try:
            student = Student.objects.get(student_id=_student_id)
            response = {
                'status': True,
                'info': S_QUERY_SUCCEED,
                'student_id': student.student_id,
                'account': student.account,
                'name': student.name,
                'gender': student.gender,
                'school': student.school,
                'department': student.department,
                'major': student.major,
                'degree': student.degree,
                'auth_state': student.auth_state,
            }
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Student.DoesNotExist:
            response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
    else:
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=401)
        try:
            teacher = Teacher.objects.get(user=user)
            response = {
                'status': True,
                'info': S_QUERY_SUCCEED,
                'teacher_id': teacher.teacher_id,
                'account': teacher.account,
                'name': teacher.name,
                'gender': teacher.gender,
                'school': teacher.school,
                'department': teacher.department,
                'title': teacher.title,
                'auth_state': teacher.auth_state,
            }
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Teacher.DoesNotExist:
            pass
        try:
            student = Student.objects.get(user=user)
            response = {
                'status': True,
                'info': S_QUERY_SUCCEED,
                'student_id': student.student_id,
                'account': student.account,
                'name': student.name,
                'gender': student.gender,
                'school': student.school,
                'department': student.department,
                'major': student.major,
                'degree': student.degree,
                'auth_state': student.auth_state,
            }
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Student.DoesNotExist:
            pass
        response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@post_required
@login_required
def update_info(request):
    # *** 参数获取 ***
    _name = request.POST.get('name')
    _gender = request.POST.get('gender')
    _school = request.POST.get('school')
    _department = request.POST.get('department')
    _title = request.POST.get('title')
    _major = request.POST.get('major')
    _degree = request.POST.get('degree')
    # *** 合法性检测 ***
    if not check_optional(_name, _gender, _school, _department, _title, _major, _degree):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_enumeration(_gender, ('M', 'F', 'U')) or not check_enumeration(_title, ('TA', 'LT', 'AP', 'PP')) or not check_enumeration(_degree, ('UG', 'MT', 'DT')):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    user = request.user
    try:
        teacher = Teacher.objects.get(user=user)
        if _name is not None:
            teacher.name = _name
        if _gender is not None:
            teacher.gender = _gender
        if _school is not None:
            teacher.school = _school
        if _department is not None:
            teacher.department = _department
        if _title is not None:
            teacher.title = _title
        teacher.save()
        response = {'status': True, 'info': S_UPDATE_SUCCEED}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        if _name is not None:
            student.name = _name
        if _gender is not None and _gender in ('M', 'F', 'U'):
            student.gender = _gender
        if _school is not None:
            student.school = _school
        if _department is not None:
            student.department = _department
        if _major is not None:
            student.major = _major
        if _degree is not None:
            student.degree = _degree
        student.save()
        response = {'status': True, 'info': S_UPDATE_SUCCEED}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Student.DoesNotExist:
        pass
    response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
def get_info_plus(request):
    # *** 参数获取 ***
    _type = request.GET.get('type')
    _teacher_id = request.GET.get('teacher_id')
    _student_id = request.GET.get('student_id')
    # *** 合法性检测 ***
    if not check_necessary(_type):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_enumeration(_type, ('T', 'S', 'I')):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if (_type == 'T' and _teacher_id is None) or (_type == 'S' and _student_id is None):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    if _type == 'T':
        try:
            teacher = Teacher.objects.get(teacher_id=_teacher_id)
            response = {
                'status': True,
                'info': S_QUERY_SUCCEED,
                'signature': teacher.signature,
                'phone': teacher.phone,
                'email': teacher.email,
                'homepage': teacher.homepage,
                'address': teacher.address,
                'introduction': teacher.introduction,
                'research_fields': teacher.research_fields,
                'research_achievements': teacher.research_achievements,
                'promotional_video_url': teacher.promotional_video_url,
                'follow_number': teacher.follows.count(),
                'fan_number': teacher.user.teacher_fans.count() + teacher.user.student_fans.count(),
            }
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Teacher.DoesNotExist:
            response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
    elif _type == 'S':
        try:
            student = Student.objects.get(student_id=_student_id)
            response = {
                'status': True,
                'info': S_QUERY_SUCCEED,
                'signature': student.signature,
                'phone': student.phone,
                'email': student.email,
                'homepage': student.homepage,
                'address': student.address,
                'introduction': student.introduction,
                'research_interest': student.research_interest,
                'research_experience': student.research_experience,
                'promotional_video_url': student.promotional_video_url,
                'follow_number': student.follows.count(),
                'fan_number': student.user.teacher_fans.count() + student.user.student_fans.count(),
            }
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Student.DoesNotExist:
            response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
    else:
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=401)
        try:
            teacher = Teacher.objects.get(user=user)
            response = {
                'status': True,
                'info': S_QUERY_SUCCEED,
                'signature': teacher.signature,
                'phone': teacher.phone,
                'email': teacher.email,
                'homepage': teacher.homepage,
                'address': teacher.address,
                'introduction': teacher.introduction,
                'research_fields': teacher.research_fields,
                'research_achievements': teacher.research_achievements,
                'promotional_video_url': teacher.promotional_video_url,
                'teacher_number': teacher.teacher_number,
                'id_number': teacher.id_number,
                'follow_number': teacher.follows.count(),
                'fan_number': teacher.user.teacher_fans.count() + teacher.user.student_fans.count(),
            }
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Teacher.DoesNotExist:
            pass
        try:
            student = Student.objects.get(user=user)
            response = {
                'status': True,
                'info': S_QUERY_SUCCEED,
                'signature': student.signature,
                'phone': student.phone,
                'email': student.email,
                'homepage': student.homepage,
                'address': student.address,
                'introduction': student.introduction,
                'research_interest': student.research_interest,
                'research_experience': student.research_experience,
                'promotional_video_url': student.promotional_video_url,
                'student_number': student.student_number,
                'id_number': student.id_number,
                'follow_number': student.follows.count(),
                'fan_number': student.user.teacher_fans.count() + student.user.student_fans.count(),
            }
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except Student.DoesNotExist:
            pass
        response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@post_required
@login_required
def update_info_plus(request):
    # *** 参数获取 ***
    _signature = request.POST.get('signature')
    _phone = request.POST.get('phone')
    _email = request.POST.get('email')
    _homepage = request.POST.get('homepage')
    _address = request.POST.get('address')
    _introduction = request.POST.get('introduction')
    _research_fields = request.POST.get('research_fields')
    _research_achievements = request.POST.get('research_achievements')
    _research_interest = request.POST.get('research_interest')
    _research_experience = request.POST.get('research_experience')
    _promotional_video_url = request.POST.get('promotional_video_url')
    # *** 合法性检测 ***
    if not check_optional(_signature, _phone, _email, _homepage, _address,
                          _introduction, _research_fields, _research_achievements, _research_interest, _research_experience, _promotional_video_url):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    user = request.user
    try:
        teacher = Teacher.objects.get(user=user)
        if _signature is not None:
            teacher.signature = _signature
        if _phone is not None:
            teacher.phone = _phone
        if _email is not None:
            teacher.email = _email
        if _homepage is not None:
            teacher.homepage = _homepage
        if _address is not None:
            teacher.address = _address
        if _introduction is not None:
            teacher.introduction = _introduction
        if _research_fields is not None:
            teacher.research_fields = _research_fields
        if _research_achievements is not None:
            teacher.research_achievements = _research_achievements
        if _promotional_video_url is not None:
            teacher.promotional_video_url = _promotional_video_url
        teacher.save()
        response = {'status': True, 'info': S_UPDATE_SUCCEED}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        if _signature is not None:
            student.signature = _signature
        if _phone is not None:
            student.phone = _phone
        if _email is not None:
            student.email = _email
        if _homepage is not None:
            student.homepage = _homepage
        if _address is not None:
            student.address = _address
        if _introduction is not None:
            student.introduction = _introduction
        if _research_interest is not None:
            student.research_interest = _research_interest
        if _research_experience is not None:
            student.research_experience = _research_experience
        if _promotional_video_url is not None:
            student.promotional_video_url = _promotional_video_url
        student.save()
        response = {'status': True, 'info': S_UPDATE_SUCCEED}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Student.DoesNotExist:
        pass
    response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@get_required
def get_info_picture(request):
    # *** 参数获取 ***
    _type = request.GET.get('type')
    _teacher_id = request.GET.get('teacher_id')
    _student_id = request.GET.get('student_id')
    # *** 合法性检测 ***
    if not check_necessary(_type):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_enumeration(_type, ('T', 'S', 'I')):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if (_type == 'T' and _teacher_id is None) or (_type == 'S' and _student_id is None):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    if _type == 'T':
        try:
            teacher = Teacher.objects.get(teacher_id=_teacher_id)
            return HttpResponse(teacher.picture_128px.file, content_type='image/jpeg')
            # return HttpResponse(teacher.picture.file, content_type='image/jpeg')
        except Teacher.DoesNotExist:
            response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except (ValueError, TypeError):
            return HttpResponse(None, content_type='image/jpeg')
    elif _type == 'S':
        try:
            student = Student.objects.get(student_id=_student_id)
            return HttpResponse(student.picture_128px.file, content_type='image/jpeg')
            # return HttpResponse(student.picture.file, content_type='image/jpeg')
        except Student.DoesNotExist:
            response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        except (ValueError, TypeError):
            return HttpResponse(None, content_type='image/jpeg')
    else:
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=401)
        try:
            teacher = Teacher.objects.get(user=user)
            return HttpResponse(teacher.picture_128px.file, content_type='image/jpeg')
            # return HttpResponse(teacher.picture.file, content_type='image/jpeg')
        except Teacher.DoesNotExist:
            pass
        except (ValueError, TypeError):
            return HttpResponse(None, content_type='image/jpeg')
        try:
            student = Student.objects.get(user=user)
            return HttpResponse(student.picture_128px.file, content_type='image/jpeg')
            # return HttpResponse(student.picture.file, content_type='image/jpeg')
        except Student.DoesNotExist:
            pass
        except (ValueError, TypeError):
            return HttpResponse(None, content_type='image/jpeg')
        response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@post_required
@login_required
def update_info_picture(request):
    # *** 参数获取 ***
    _picture = request.FILES.get('picture')
    # *** 请求处理 ***
    user = request.user
    try:
        teacher = Teacher.objects.get(user=user)
        if _picture is not None:
            teacher.picture = _picture
            teacher.save()
        response = {'status': True, 'info': S_UPDATE_SUCCEED}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Teacher.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        if _picture is not None:
            student.picture = _picture
            student.save()
        response = {'status': True, 'info': S_UPDATE_SUCCEED}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Student.DoesNotExist:
        pass
    response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
    return HttpResponse(json.dumps(response, ensure_ascii=False))
