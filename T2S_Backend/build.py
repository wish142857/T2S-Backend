import random
import requests

'''
数据自动创建脚本
'''

SERVER_HOST = "http://127.0.0.1:8000"
TEACHER_NUMBER = 40  # 创建导师用户数量
STUDENT_NUMBER = 40  # 创建学生用户数量
FOLLOW_NUMBER = 5  # 创建关注关系数量/每个用户/分别对导师或学生
INTENTION_NUMBER = 2  # 创建意向数量/每个用户
MESSAGE_NUMBER = 5  # 创建消息数量/每个用户
DEFAULT_STRING = '这是一句消息'  # 默认填充字符串
DEFAULT_PASSWORD = 'P12345'  # 默认密码
DEFAULT_SIGNATURE = '这是一段签名。'  # 默认签名
DEFAULT_PHONE = '1XXXXXXXXXX'  # 默认电话
DEFAULT_EMAIL = 'XXX@XXX.edu.cn'  # 默认邮箱
DEFAULT_HOMEPAGE = 'http://XXX.com'  # 默认主页
DEFAULT_ADDRESS = 'XX区'  # 默认地址
DEFAULT_INTRODUCTION = '这是一段个人介绍。'  # 默认个人介绍
DEFAULT_PROMOTIONAL_VIDEO_URL = 'http://jzvd.nathen.cn/c6e3dc12a1154626b3476d9bf3bd7266/6b56c5f0dc31428083757a45764763b0-5287d2089db37e62345123a1be272f8b.mp4'  # 默认宣传视频URL
DEFAULT_RESEARCH_EXPERIENCE = '这是一段研究经历。'  # 默认研究经历
DEFAULT_RESEARCH_ACHIEVEMENT = '这是一段研究成果。'  # 默认研究成果


def POST(url: str, param: dict, cookie):
    return requests.post(url=SERVER_HOST + url, data=param, cookies=cookie)


def OK(response):
    if response.status_code == 200:
        return response.json()['status']
    return False


def build_teacher():
    # *** 数据初始化 ***
    s_number = 0
    f_number = 0
    name = ['李', '王', '张', '刘', '陈', '杨', '赵', '黄', '周', '吴',
            '徐', '孙', '胡', '朱', '高', '林', '何', '郭', '马', '罗',
            '梁', '宋', '郑', '谢', '韩', '唐', '冯', '于', '董', '萧',
            '程', '曹', '袁', '邓', '许', '傅', '沈', '曾', '彭', '吕']
    # *** 创建导师 ***
    print('>>> 【开始】正在随机生成导师数据...')
    for i in range(TEACHER_NUMBER):
        # * 注册 *
        random_name = random.choice(name)
        name.remove(random_name)
        param = {'type': 'T', 'account': 'T' + str(i), 'password': DEFAULT_PASSWORD, 'name': random_name + '老师'}
        if not OK(POST('/api/user/logon', param, None)):
            print('>>> 【失败】导师%s注册失败！' % ('S' + str(i)))
            f_number = f_number + 1
            continue
        # * 登录 *
        param = {'type': 'T', 'account': 'T' + str(i), 'password': DEFAULT_PASSWORD}
        response = POST('/api/user/login', param, None)
        if not OK(response):
            print('>>> 【失败】导师%s登录失败！' % ('T' + str(i)))
            f_number = f_number + 1
            continue
        cookies = response.cookies
        # * 修改信息 *
        param = {'gender': get_random_gender(), 'school': get_random_school(), 'department': get_random_department(), 'title': get_random_title()}
        if not OK(POST('/api/user/update_info', param, cookies)):
            print('>>> 【失败】导师%s修改失败！' % ('T' + str(i)))
            f_number = f_number + 1
            continue
        param = {'signature': DEFAULT_SIGNATURE, 'phone': DEFAULT_PHONE, 'email': DEFAULT_EMAIL, 'homepage': DEFAULT_HOMEPAGE,
                 'address': DEFAULT_ADDRESS, 'introduction': DEFAULT_INTRODUCTION, 'promotional_video_url': DEFAULT_PROMOTIONAL_VIDEO_URL,
                 'research_fields': get_random_research_fields(), 'research_achievements': DEFAULT_RESEARCH_ACHIEVEMENT}
        if not OK(POST('/api/user/update_info_plus', param, cookies)):
            print('>>> 【失败】导师%s修改失败！' % ('T' + str(i)))
            f_number = f_number + 1
            continue
        # * 用户认证 *
        param = {'teacher_number': '2017', 'id_number': random.choice(['2017', '2018'])}
        POST('/api/user/user_auth', param, cookies)
        # * 注销 *
        if not OK(POST('/api/user/logout', {}, cookies)):
            print('>>> 【失败】导师%s注销失败！' % ('T' + str(i)))
            f_number = f_number + 1
            continue
        print('>>> 【成功】导师%s生成成功！' % ('T' + str(i)))
        s_number = s_number + 1
    print('>>> 【结束】随机生成导师完毕: 成功 %d/%d 个。' % (s_number, s_number + f_number))


def build_student():
    # *** 数据初始化 ***
    s_number = 0
    f_number = 0
    name = ['李', '王', '张', '刘', '陈', '杨', '赵', '黄', '周', '吴',
            '徐', '孙', '胡', '朱', '高', '林', '何', '郭', '马', '罗',
            '梁', '宋', '郑', '谢', '韩', '唐', '冯', '于', '董', '萧',
            '程', '曹', '袁', '邓', '许', '傅', '沈', '曾', '彭', '吕']
    # *** 创建学生 ***
    print('>>> 【开始】正在随机生成学生数据...')
    for i in range(STUDENT_NUMBER):
        # * 注册 *
        random_name = random.choice(name)
        name.remove(random_name)
        param = {'type': 'S', 'account': 'S' + str(i), 'password': DEFAULT_PASSWORD, 'name': random_name + '同学'}
        if not OK(POST('/api/user/logon', param, None)):
            print('>>> 【失败】学生%s注册失败！' % ('S' + str(i)))
            f_number = f_number + 1
            continue
        # * 登录 *
        param = {'type': 'S', 'account': 'S' + str(i), 'password': DEFAULT_PASSWORD}
        response = POST('/api/user/login', param, None)
        if not OK(response):
            print('>>> 【失败】学生%s登录失败！' % ('S' + str(i)))
            f_number = f_number + 1
            continue
        cookies = response.cookies
        # * 修改信息 *
        major = get_random_major()
        param = {'gender': get_random_gender(), 'school': get_random_school(), 'department': major + '院',
                 'major': major, 'degree': get_random_degree()}
        if not OK(POST('/api/user/update_info', param, cookies)):
            print('>>> 【失败】学生%s修改失败！' % ('S' + str(i)))
            f_number = f_number + 1
            continue
        param = {'signature': DEFAULT_SIGNATURE, 'phone': DEFAULT_PHONE, 'email': DEFAULT_EMAIL, 'homepage': DEFAULT_HOMEPAGE,
                 'address': DEFAULT_ADDRESS, 'introduction': DEFAULT_INTRODUCTION, 'promotional_video_url': DEFAULT_PROMOTIONAL_VIDEO_URL,
                 'research_interest': get_random_research_interest(), 'research_experience': DEFAULT_RESEARCH_EXPERIENCE}
        if not OK(POST('/api/user/update_info_plus', param, cookies)):
            print('>>> 【失败】学生%s修改失败！' % ('S' + str(i)))
            f_number = f_number + 1
            continue
        # * 用户认证 *
        param = {'student_number': '2017', 'id_number': random.choice(['2017', '2018'])}
        POST('/api/user/user_auth', param, cookies)
        # * 注销 *
        if not OK(POST('/api/user/logout', {}, cookies)):
            print('>>> 【失败】学生%s注销失败！' % ('S' + str(i)))
            f_number = f_number + 1
            continue
        print('>>> 【成功】学生%s生成成功！' % ('S' + str(i)))
        s_number = s_number + 1
    print('>>> 【结束】随机生成学生完毕: 成功 %d/%d 个。' % (s_number, s_number + f_number))


def build_follow():
    # *** 创建导师关注关系 ***
    print('>>> 【开始】正在生成导师关注关系...')
    s_number = 0
    f_number = 0
    for t in range(TEACHER_NUMBER):
        # 登录
        param = {'type': 'T', 'account': 'T' + str(t), 'password': DEFAULT_PASSWORD}
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
        print('>>> 【完毕】导师%s生成关注关系完毕！' % ('T' + str(t)))
    print('>>> 【结束】随机生成导师关注关系完毕: 成功 %d/%d 个。' % (s_number, s_number + f_number))
    # *** 创建学生关注关系 ***
    print('>>> 【开始】正在生成学生关注关系...')
    s_number = 0
    f_number = 0
    for s in range(STUDENT_NUMBER):
        # 登录
        param = {'type': 'S', 'account': 'S' + str(s), 'password': DEFAULT_PASSWORD}
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
        print('>>> 【完毕】学生%s生成关注关系完毕！' % ('S' + str(s)))
    print('>>> 【结束】随机生成学生关注关系完毕: 成功 %d/%d 个。' % (s_number, s_number + f_number))


def build_intention():
    # *** 创建导师招收意向 ***
    print('>>> 【开始】正在生成导师招收意向...')
    s_number = 0
    f_number = 0
    for t in range(TEACHER_NUMBER):
        # 登录
        param = {'type': 'T', 'account': 'T' + str(t), 'password': DEFAULT_PASSWORD}
        response = POST('/api/user/login', param, None)
        if not OK(response):
            f_number = f_number + 1
            continue
        cookies = response.cookies
        # 创建
        for i in range(INTENTION_NUMBER):
            param = {'recruitment_type': get_random_recruitment_type(), 'recruitment_number': get_random_number(),
                     'research_fields': get_random_research_fields(), 'introduction': DEFAULT_INTRODUCTION, 'intention_state': get_random_intention_state()}
            response = POST('/api/intention/create_recruit_intention', param, cookies)
            if OK(response):
                s_number = s_number + 1
            else:
                f_number = f_number + 1
        # 注销
        POST('/api/user/logout', {}, cookies)
        print('>>> 【完毕】导师%s生成招收意向完毕！' % ('T' + str(t)))
    print('>>> 【结束】随机生成导师招收意向完毕: 成功 %d/%d 个。' % (s_number, s_number + f_number))
    # *** 创建学生申请意向 ***
    print('>>> 【开始】正在生成学生申请意向...')
    s_number = 0
    f_number = 0
    for s in range(STUDENT_NUMBER):
        # 登录
        param = {'type': 'S', 'account': 'S' + str(s), 'password': DEFAULT_PASSWORD}
        response = POST('/api/user/login', param, None)
        if not OK(response):
            f_number = f_number + 1
            continue
        cookies = response.cookies
        # 创建
        for i in range(INTENTION_NUMBER):
            param = {'research_interests': get_random_research_interest(), 'introduction': DEFAULT_INTRODUCTION, 'intention_state': get_random_intention_state()}
            response = POST('/api/intention/create_apply_intention', param, cookies)
            if OK(response):
                s_number = s_number + 1
            else:
                f_number = f_number + 1
        # 注销
        POST('/api/user/logout', {}, cookies)
        print('>>> 【完毕】学生%s生成申请意向完毕！' % ('S' + str(s)))
    print('>>> 【结束】随机生成学生申请意向完毕: 成功 %d/%d 个。' % (s_number, s_number + f_number))


def build_conversation():
    # *** 创建导师会话消息 ***
    print('>>> 【开始】正在生成导师会话消息...')
    s_number = 0
    f_number = 0
    for t in range(TEACHER_NUMBER):
        # 登录
        param = {'type': 'T', 'account': 'T' + str(t), 'password': DEFAULT_PASSWORD}
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
        print('>>> 【完毕】导师%s生成会话消息完毕！' % ('T' + str(t)))
    print('>>> 【结束】随机生成导师会话消息完毕: 成功 %d/%d 个。' % (s_number, s_number + f_number))
    # *** 创建学生会话消息 ***
    print('>>> 【开始】正在生成学生会话消息...')
    s_number = 0
    f_number = 0
    for s in range(STUDENT_NUMBER):
        # 登录
        param = {'type': 'S', 'account': 'S' + str(s), 'password': DEFAULT_PASSWORD}
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
        print('>>> 【完毕】学生%s生成会话消息完毕！' % ('S' + str(s)))
    print('>>> 【结束】随机生成学生会话消息完毕: 成功 %d/%d 个。' % (s_number, s_number + f_number))


def get_random_number() -> str:
    return random.choice(['0', '1', '2', '3', '4', '5'])


def get_random_teacher_id() -> str:
    return str(random.randint(1, TEACHER_NUMBER))


def get_random_student_id() -> str:
    return str(random.randint(1, STUDENT_NUMBER))


def get_random_t_or_s_type() -> str:
    return random.choice(['T', 'S'])


def get_random_recruitment_type() -> str:
    return random.choice(['UG', 'MT', 'DT'])


def get_random_intention_state() -> str:
    return random.choice(['O', 'S', 'F'])


def get_random_information_state() -> str:
    return random.choice(['N', 'R', 'H'])


def get_random_gender() -> str:
    return random.choice(['M', 'F', 'U'])


def get_random_school() -> str:
    return random.choice(['北京大学', '清华大学', '复旦大学', '上海交通大学',
                          '南京大学', '浙江大学', '中国科学技术大学', '哈尔滨工业大学', '西安交通大学'])


def get_random_department() -> str:
    return random.choice(['哲学院', '经济学院', '法学院', '教育学院', '文学院', '历史学院',
                          '理学院', '工学院', '农学院', '医学院', '军事学院', '管理学院', '艺术学院'])


def get_random_title() -> str:
    return random.choice(['TA', 'LT', 'AP', 'PP'])


def get_random_major() -> str:
    return random.choice(['哲学', '经济学', '法学', '教育学', '文学', '历史学',
                          '理学', '工学', '农学', '医学', '军事学', '管理学', '艺术学'])


def get_random_degree() -> str:
    return random.choice(['UG', 'MT', 'DT'])


def get_random_research_fields() -> str:
    choices = ['哲学', '经济学', '法学', '教育学', '文学', '历史学', '理学', '工学', '农学', '医学', '军事学', '管理学', '艺术学']
    field_1 = random.choice(choices)
    choices.remove(field_1)
    field_2 = random.choice(choices)
    choices.remove(field_2)
    field_3 = random.choice(choices)
    choices.remove(field_3)
    return ';'.join((field_1, field_2, field_3))


def get_random_research_interest() -> str:
    choices = ['哲学', '经济学', '法学', '教育学', '文学', '历史学', '理学', '工学', '农学', '医学', '军事学', '管理学', '艺术学']
    field_1 = random.choice(choices)
    choices.remove(field_1)
    field_2 = random.choice(choices)
    choices.remove(field_2)
    field_3 = random.choice(choices)
    choices.remove(field_3)
    return ';'.join((field_1, field_2, field_3))


def main():
    build_teacher()
    build_student()
    build_follow()
    build_intention()
    build_conversation()
    pass


if __name__ == '__main__':
    main()
