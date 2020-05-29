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
def create_recruit_intention(request):
    # TODO
    pass


@ post_required
def delete_recruit_intention(request):
    # TODO
    pass


@ post_required
def update_recruit_intention(request):
    # TODO
    pass


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
    # TODO
    pass


@ post_required
def delete_apply_intention(request):
    # TODO
    pass


@ post_required
def update_apply_intention(request):
    # TODO
    pass
