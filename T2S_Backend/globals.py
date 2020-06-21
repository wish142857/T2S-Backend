"""
全局变量
"""

N_RECOMMEND_RANDOM_NUMBER = 10                  # 推荐随机数据数量
N_RECOMMEND_MATCH_NUMBER = 4                    # 推荐匹配数量
N_DEFAULT_GET_SEARCH_RECORD_NUMBER = 10         # 默认获取搜索记录数量
N_DEFAULT_GET_HOT_SEARCH_RECORD_NUMBER = 10     # 默认获取热门搜索记录数量

S_LOGON_SUCCEED = '[成功] 注册成功！'
S_LOGIN_SUCCEED = '[成功] 登录成功！'
S_LOGOUT_SUCCEED = '[成功] 注销成功！'
S_AUTH_SUCCEED = '[成功] 认证成功！'
S_CHANGE_PASSWORD_SUCCEED = '[成功] 修改密码成功！'
S_QUERY_SUCCEED = '[成功] 查询成功！'
S_CREATE_SUCCEED = '[成功] 创建成功！'
S_DELETE_SUCCEED = '[成功] 删除成功！'
S_UPDATE_SUCCEED = '[成功] 修改成功！'
S_SEND_SUCCEED = '[成功] 发送成功！'
S_SEARCH_SUCCEED = '[成功] 搜索成功！'
S_RECOMMEND_SUCCEED = '[成功] 推荐成功！'

F_INTERNAL_ERROR = '[失败] 内部错误！'
F_MISSING_PARAMETER = '[失败] 缺少必要参数！'
F_ERROR_PARAMETER = '[失败] 错误参数格式！'
F_ERROR_NOT_FOUND = '[失败] 未找到数据！'
F_ERROR_UNKNOWN_USER = '[失败] 未知用户！'
F_DUPLICATE_USERNAME = '[失败] 重复用户名！'
F_ERROR_PASSWORD = '[失败] 错误密码！'
F_ERROR_USERNAME_OR_PASSWORD = '[失败] 错误用户名或密码！'
F_AUTH_FAIL = '[失败] 认证失败！'
F_CREATE_FAIL = '[失败] 创建失败！'
F_DELETE_FAIL = '[失败] 删除失败！'
F_UPDATE_FAIL = '[失败] 修改失败！'
F_NOT_IMPLEMENTED = '[失败] 功能未实现！'

I_NEW_LOGIN = '【新用户|%s】\n新账户<%s>注册成功！欢迎您~'
I_NEW_FOLLOW = '【新关注|%s】\n用户<%s(%s)>关注了您。'
I_NEW_INTENTION = '【新意向|%s】\n您关注的用户<%s(%s)>更新了意向。'
I_NEW_PASSWORD = '【新密码|%s】\n您的账户<%s(%s)>密码已成功修改。'
