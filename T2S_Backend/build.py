import random
import requests

'''
数据自动创建脚本
'''

SERVER_HOST = "http://127.0.0.1:8000"
TEACHER_NUMBER = 10         # 创建导师用户数量
STUDENT_NUMBER = 10         # 创建学生用户数量
INTENTION_NUMBER = 3        # 创建意向数量/每个用户
INFORMATION_NUMBER = 3      # 创建系统信息数量/每个用户
MESSAGE_NUMBER = 10         # 创建会话消息数量/每个用户
FOLLOW_NUMBER = 5           # 创建关注关系数量/每个用户/分别对导师或学生
DEFAULT_STRING = 'Empty'    # 默认填充字符串


def POST(url: str, param: dict, cookie):
    return requests.post(url=SERVER_HOST + url, data=param, cookies=cookie)


def OK(response):
    if response.status_code == 200:
        return response.json()['status']
    return False


def create_user():
    # *** 创建导师用户 ***
    s_number = 0
    f_number = 0
    for t in range(TEACHER_NUMBER):
        param = {'type': 'T', 'account': 'T' + str(t), 'password': 'T' + str(t), 'name': 'T' + str(t)}
        if OK(POST('/api/user/logon', param, None)):
            s_number = s_number + 1
        else:
            f_number = f_number + 1
    print('@ 注册导师: 成功 %d/%d 个.' % (s_number, s_number + f_number))
    # *** 创建学生用户 ***
    s_number = 0
    f_number = 0
    for s in range(STUDENT_NUMBER):
        param = {'type': 'S', 'account': 'S' + str(s), 'password': 'S' + str(s), 'name': 'S' + str(s)}
        if OK(POST('/api/user/logon', param, None)):
            s_number = s_number + 1
        else:
            f_number = f_number + 1
    print('@ 注册学生: 成功 %d/%d 个.' % (s_number, s_number + f_number))


def create_intention():
    # *** 创建导师招收意向 ***
    s_number = 0
    f_number = 0
    for t in range(TEACHER_NUMBER):
        # 登录
        param = {'type': 'T', 'account': 'T' + str(t), 'password': 'T' + str(t)}
        response = POST('/api/user/login', param, None)
        if not OK(response):
            f_number = f_number + 1
            continue
        cookies = response.cookies
        # 创建
        for i in range(INTENTION_NUMBER):
            param = {'recruitment_type': get_random_recruitment_type(), 'recruitment_number': get_random_number(),
                     'research_fields': DEFAULT_STRING, 'introduction': DEFAULT_STRING, 'intention_state': get_random_intention_state()}
            response = POST('/api/intention/create_recruit_intention', param, cookies)
            if OK(response):
                s_number = s_number + 1
            else:
                f_number = f_number + 1
        # 注销
        POST('/api/user/logout', {}, cookies)
    print('@ 创建导师招收意向: 成功 %d/%d 个.' % (s_number, s_number + f_number))
    # *** 创建学生申请意向 ***
    s_number = 0
    f_number = 0
    for s in range(STUDENT_NUMBER):
        # 登录
        param = {'type': 'S', 'account': 'S' + str(s), 'password': 'S' + str(s)}
        response = POST('/api/user/login', param, None)
        if not OK(response):
            f_number = f_number + 1
            continue
        cookies = response.cookies
        # 创建
        for i in range(INTENTION_NUMBER):
            param = {'research_interests': DEFAULT_STRING, 'introduction': DEFAULT_STRING, 'intention_state': get_random_intention_state()}
            response = POST('/api/intention/create_apply_intention', param, cookies)
            if OK(response):
                s_number = s_number + 1
            else:
                f_number = f_number + 1
        # 注销
        POST('/api/user/logout', {}, cookies)
    print('@ 创建学生申请意向: 成功 %d/%d 个.' % (s_number, s_number + f_number))


def create_information():
    # *** 创建导师系统信息 ***
    s_number = 0
    f_number = 0
    for t in range(TEACHER_NUMBER):
        # 创建
        for i in range(INFORMATION_NUMBER):
            param = {'information_type': 'T', 'information_content': DEFAULT_STRING, 'information_state': get_random_information_state(),
                     'receiver_type': 'T', 'receiver_id': str(t + 1)}
            response = POST('/api/information/create_information', param, None)
            if OK(response):
                s_number = s_number + 1
            else:
                f_number = f_number + 1
    print('@ 创建导师系统信息: 成功 %d/%d 个.' % (s_number, s_number + f_number))
    # *** 创建学生系统信息 ***
    s_number = 0
    f_number = 0
    for s in range(STUDENT_NUMBER):
        # 创建
        for i in range(INFORMATION_NUMBER):
            param = {'information_type': 'T', 'information_content': DEFAULT_STRING, 'information_state': get_random_information_state(),
                     'receiver_type': 'S', 'receiver_id': str(s + 1)}
            response = POST('/api/information/create_information', param, None)
            if OK(response):
                s_number = s_number + 1
            else:
                f_number = f_number + 1
    print('@ 创建学生系统信息: 成功 %d/%d 个.' % (s_number, s_number + f_number))


def create_conversation():
    # *** 创建导师会话消息 ***
    s_number = 0
    f_number = 0
    for t in range(TEACHER_NUMBER):
        # 登录
        param = {'type': 'T', 'account': 'T' + str(t), 'password': 'T' + str(t)}
        response = POST('/api/user/login', param, None)
        if not OK(response):
            f_number = f_number + 1
            continue
        cookies = response.cookies
        # 创建
        for i in range(MESSAGE_NUMBER):
            object_type = get_random_t_or_s_type()
            if object_type == 'T':
                param = {'object_id': get_random_teacher_id(), 'object_type': 'T', 'message_type': 'T', 'message_content': DEFAULT_STRING}
            else:
                param = {'object_id': get_random_student_id(), 'object_type': 'S', 'message_type': 'T', 'message_content': DEFAULT_STRING}
            response = POST('/api/conversation/send_message', param, cookies)
            if OK(response):
                s_number = s_number + 1
            else:
                f_number = f_number + 1
        # 注销
        POST('/api/user/logout', {}, cookies)
    print('@ 创建导师会话消息: 成功 %d/%d 个.' % (s_number, s_number + f_number))
    # *** 创建学生会话消息 ***
    s_number = 0
    f_number = 0
    for s in range(STUDENT_NUMBER):
        # 登录
        param = {'type': 'S', 'account': 'S' + str(s), 'password': 'S' + str(s)}
        response = POST('/api/user/login', param, None)
        if not OK(response):
            f_number = f_number + 1
            continue
        cookies = response.cookies
        # 创建
        for i in range(MESSAGE_NUMBER):
            object_type = get_random_t_or_s_type()
            if object_type == 'T':
                param = {'object_id': get_random_teacher_id(), 'object_type': 'T', 'message_type': 'T', 'message_content': DEFAULT_STRING}
            else:
                param = {'object_id': get_random_student_id(), 'object_type': 'S', 'message_type': 'T', 'message_content': DEFAULT_STRING}
            response = POST('/api/conversation/send_message', param, cookies)
            if OK(response):
                s_number = s_number + 1
            else:
                f_number = f_number + 1
        # 注销
        POST('/api/user/logout', {}, cookies)
    print('@ 创建学生会话消息: 成功 %d/%d 个.' % (s_number, s_number + f_number))


def create_follow():
    # *** 创建导师关注关系 ***
    s_number = 0
    f_number = 0
    for t in range(TEACHER_NUMBER):
        # 登录
        param = {'type': 'T', 'account': 'T' + str(t), 'password': 'T' + str(t)}
        response = POST('/api/user/login', param, None)
        if not OK(response):
            f_number = f_number + 1
            continue
        cookies = response.cookies
        # 创建
        for i in range(FOLLOW_NUMBER):
            param = {'teacher_id': get_random_teacher_id(), 'student_id': get_random_student_id()}
            response = POST('/api/follow/add_to_watch', param, cookies)
            if OK(response):
                s_number = s_number + 1
            else:
                f_number = f_number + 1
        # 注销
        POST('/api/user/logout', {}, cookies)
    print('@ 创建导师关注关系: 成功 %d/%d 个.' % (s_number, s_number + f_number))
    # *** 创建学生关注关系 ***
    s_number = 0
    f_number = 0
    for s in range(STUDENT_NUMBER):
        # 登录
        param = {'type': 'S', 'account': 'S' + str(s), 'password': 'S' + str(s)}
        response = POST('/api/user/login', param, None)
        if not OK(response):
            f_number = f_number + 1
            continue
        cookies = response.cookies
        # 创建
        for i in range(FOLLOW_NUMBER):
            param = {'teacher_id': get_random_teacher_id(), 'student_id': get_random_student_id()}
            response = POST('/api/follow/add_to_watch', param, cookies)
            if OK(response):
                s_number = s_number + 1
            else:
                f_number = f_number + 1
        # 注销
        POST('/api/user/logout', {}, cookies)
    print('@ 创建学生关注关系: 成功 %d/%d 个.' % (s_number, s_number + f_number))


def get_random_number() -> str:
    return random.choice(['0', '1', '2', '3', '4', '5'])


def get_random_teacher_id() -> str:
    return str(random.randint(1, TEACHER_NUMBER))


def get_random_student_id() -> str:
    return str(random.randint(1, STUDENT_NUMBER))


def get_random_t_or_s_type() -> str:
    return random.choices(['T', 'S'])


def get_random_recruitment_type() -> str:
    return random.choice(['UG', 'MT', 'DT'])


def get_random_intention_state() -> str:
    return random.choice(['O', 'S', 'F'])


def get_random_information_state() -> str:
    return random.choices(['N', 'R', 'H'])


def main():
    create_user()
    create_intention()
    create_information()
    create_conversation()
    create_follow()


if __name__ == '__main__':
    main()
