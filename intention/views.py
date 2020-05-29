import json
from T2S_Backend.decorators import *
from T2S_Backend.globals import *
from T2S_Backend.utils import *
from user.models import Teacher, Student
from intention.models import Recruitment, Application


@ get_required
def get_recruit_intention(request):
    # *** 参数获取 ***
    _teacher_id = request.GET.get('teacher_id')
    # *** 合法性检测 ***
    if not check_necessary(_teacher_id):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    try:
        teacher = Teacher.objects.get(teacher_id=_teacher_id)
        recruitment_id_list = [r.recruitment_id for r in teacher.recruitment_set.all()]
        response = {'status': True, 'info': S_QUERY_SUCCEED, 'recruitment_id_list': recruitment_id_list}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Teacher.DoesNotExist:
        response = {'status': False, 'info': F_ERROR_NOT_FOUND}
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@ get_required
def get_recruit_intention_detail(request):
    # *** 参数获取 ***
    _recruitment_id = request.GET.get('_recruitment_id')
    # *** 合法性检测 ***
    if not check_necessary(_recruitment_id):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    try:
        recruitment = Recruitment.objects.get(recruitment_id=_recruitment_id)
        response = {
            'status': True,
            'info': S_QUERY_SUCCEED,
            'recruitment_type': recruitment.recruitment_type,
            'recruitment_number': recruitment.recruitment_number,
            'research_fields': recruitment.research_fields,
            'introduction': recruitment.introduction,
            'intention_state': recruitment.intention_state,
        }
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Recruitment.DoesNotExist:
        response = {'status': False, 'info': F_ERROR_NOT_FOUND}
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@ post_required
@ login_required
def create_recruit_intention(request):
    # *** 参数获取 ***
    _recruitment_type = request.POST.get('recruitment_type')
    _recruitment_number = request.POST.get('recruitment_number')
    _research_fields = request.POST.get('research_fields')
    _introduction = request.POST.get('introduction')
    _intention_state = request.POST.get('intention_state')
    # *** 合法性检测 ***
    if not check_necessary(_recruitment_type, _recruitment_number, _research_fields, _introduction, _intention_state):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_enumeration(_recruitment_type, ('UG', 'MT', 'DT')) or not check_enumeration(_intention_state, ('O', 'S', 'F')):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    user = request.user
    try:
        teacher = Teacher.objects.get(user=user)
        Recruitment.objects.create(
            publisher=teacher,
            recruitment_type=_recruitment_type,
            recruitment_number=_recruitment_number,
            research_fields=_research_fields,
            introduction=_introduction,
            intention_state=_intention_state,
        )
        response = {'status': True, 'info': S_CREATE_SUCCEED}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Teacher.DoesNotExist:
        response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@ post_required
@ login_required
def delete_recruit_intention(request):
    # *** 参数获取 ***
    _recruitment_id = request.POST.get('recruitment_id')
    # *** 合法性检测 ***
    if not check_necessary(_recruitment_id):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    user = request.user
    try:
        teacher = Teacher.objects.get(user=user)
        Recruitment.objects.get(recruitment_id=_recruitment_id, publisher=teacher).delete()
        response = {'status': True, 'info': S_DELETE_SUCCEED}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except (Teacher.DoesNotExist, Recruitment.DoesNotExist):
        response = {'status': False, 'info': F_DELETE_FAIL}
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@ post_required
@ login_required
def update_recruit_intention(request):
    # *** 参数获取 ***
    _recruitment_id = request.POST.get('recruitment_id')
    _recruitment_type = request.POST.get('recruitment_type')
    _recruitment_number = request.POST.get('recruitment_number')
    _research_fields = request.POST.get('research_fields')
    _introduction = request.POST.get('introduction')
    _intention_state = request.POST.get('intention_state')
    # *** 合法性检测 ***
    if not check_necessary(_recruitment_id) or not check_optional(_recruitment_type, _recruitment_number, _research_fields, _introduction, _intention_state):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_enumeration(_recruitment_type, ('UG', 'MT', 'DT')) or not check_enumeration(_intention_state, ('O', 'S', 'F')):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    user = request.user
    try:
        teacher = Teacher.objects.get(user=user)
        recruitment = Recruitment.objects.get(recruitment_id=_recruitment_id, publisher=teacher)
        if _recruitment_type is not None:
            recruitment.recruitment_type = _recruitment_type
        if _recruitment_number is not None:
            recruitment.recruitment_number = _recruitment_number
        if _research_fields is not None:
            recruitment.research_fields = _research_fields
        if _introduction is not None:
            recruitment.introduction = _introduction
        if _intention_state is not None:
            recruitment.intention_state = _intention_state
        recruitment.save()
        response = {'status': True, 'info': S_UPDATE_SUCCEED}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except (Teacher.DoesNotExist, Recruitment.DoesNotExist):
        response = {'status': False, 'info': F_UPDATE_FAIL}
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@ get_required
def get_apply_intention(request):
    # *** 参数获取 ***
    _student_id = request.GET.get('student_id')
    # *** 合法性检测 ***
    if not check_necessary(_student_id):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    try:
        student = Student.objects.get(student_id=_student_id)
        application_id_list = [a.application_id for a in student.application_set.all()]
        response = {'status': True, 'info': S_QUERY_SUCCEED, 'application_id_list': application_id_list}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Student.DoesNotExist:
        response = {'status': False, 'info': F_ERROR_NOT_FOUND}
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@ get_required
def get_apply_intention_detail(request):
    # *** 参数获取 ***
    _application_id = request.GET.get('application_id')
    # *** 合法性检测 ***
    if not check_necessary(_application_id):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    try:
        application = Application.objects.get(application_id=_application_id)
        response = {
            'status': True,
            'info': S_QUERY_SUCCEED,
            'research_interests': application.research_interests,
            'introduction': application.introduction,
            'intention_state': application.intention_state,
        }
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Application.DoesNotExist:
        response = {'status': False, 'info': F_ERROR_NOT_FOUND}
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@ post_required
def create_apply_intention(request):
    # *** 参数获取 ***
    _research_interests = request.POST.get('research_interests')
    _introduction = request.POST.get('introduction')
    _intention_state = request.POST.get('intention_state')
    # *** 合法性检测 ***
    if not check_necessary(_research_interests, _introduction, _intention_state):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_enumeration(_intention_state, ('O', 'S', 'F')):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    user = request.user
    try:
        student = Student.objects.get(user=user)
        Application.objects.create(
            publisher=student,
            research_interests=_research_interests,
            introduction=_introduction,
            intention_state=_intention_state,
        )
        response = {'status': True, 'info': S_CREATE_SUCCEED}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Student.DoesNotExist:
        response = {'status': False, 'info': F_ERROR_UNKNOWN_USER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@ post_required
def delete_apply_intention(request):
    # *** 参数获取 ***
    _application_id = request.POST.get('application_id')
    # *** 合法性检测 ***
    if not check_necessary(_application_id):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    user = request.user
    try:
        student = Student.objects.get(user=user)
        Application.objects.get(application_id=_application_id, publisher=student).delete()
        response = {'status': True, 'info': S_DELETE_SUCCEED}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except (Student.DoesNotExist, Application.DoesNotExist):
        response = {'status': False, 'info': F_DELETE_FAIL}
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@ post_required
def update_apply_intention(request):
    # *** 参数获取 ***
    _application_id = request.POST.get('application_id')
    _research_interests = request.POST.get('research_interests')
    _introduction = request.POST.get('introduction')
    _intention_state = request.POST.get('intention_state')
    # *** 合法性检测 ***
    if not check_necessary(_application_id) or not check_optional(_research_interests, _introduction, _intention_state):
        response = {'status': False, 'info': F_MISSING_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    if not check_enumeration(_intention_state, ('O', 'S', 'F')):
        response = {'status': False, 'info': F_ERROR_PARAMETER}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # *** 请求处理 ***
    user = request.user
    try:
        student = Student.objects.get(user=user)
        application = Application.objects.get(application_id=_application_id, publisher=student)
        if _research_interests is not None:
            application._research_interests = _research_interests
        if _introduction is not None:
            application.introduction = _introduction
        if _intention_state is not None:
            application.intention_state = _intention_state
        application.save()
        response = {'status': True, 'info': S_UPDATE_SUCCEED}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    except (Student.DoesNotExist, Application.DoesNotExist):
        response = {'status': False, 'info': F_UPDATE_FAIL}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
