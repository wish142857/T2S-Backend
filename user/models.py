from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill


def custom_upload_path(instance, filename):
    class_name = instance.__class__.__name__.lower()
    return "picture/{}/{}-{}/{}".format(class_name+"s", class_name, instance.pk, filename)


class Teacher(models.Model):
    GENDER_CHOICES = [('M', 'male'), ('F', 'female'), ('U', 'unknown')]
    AUTH_STATE_CHOICES = [('UQ', 'unqualified'), ('QD', 'qualified')]
    TITLE_CHOICES = [('TA', 'assistant'), ('LT', 'lecturer'), ('AP', 'associate professor'), ('PP', 'professor')]

    teacher_id = models.AutoField(primary_key=True)                                 # 导师 ID
    user = models.OneToOneField(User, on_delete=models.CASCADE)                     # 用户账户
    follows = models.ManyToManyField(User, related_name='teacher_fans')             # 关注关系

    account = models.CharField(max_length=32, null=False, unique=True)              # 账号
    password = models.CharField(max_length=32, null=False)                          # 密码
    name = models.CharField(max_length=16, null=False)                              # 名称
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')    # 性别
    school = models.CharField(max_length=32)                                        # 学校
    department = models.CharField(max_length=32)                                    # 院系
    title = models.CharField(max_length=2, choices=TITLE_CHOICES, default='TA')     # 职务
    auth_state = models.CharField(max_length=2, choices=AUTH_STATE_CHOICES, default='UQ')  # 认证状态

    picture = models.ImageField(upload_to=custom_upload_path)                       # 头像
    signature = models.CharField(max_length=1024)                                   # 签名
    phone = models.CharField(max_length=64)                                         # 电话
    email = models.CharField(max_length=64)                                         # 邮箱
    homepage = models.CharField(max_length=128)                                     # 主页
    address = models.CharField(max_length=128)                                      # 地址
    teacher_number = models.CharField(max_length=32)                                # 工号
    id_number = models.CharField(max_length=32)                                     # 身份证号
    introduction = models.CharField(max_length=51200)                               # 个人介绍
    research_fields = models.CharField(max_length=51200)                            # 研究方向
    research_achievements = models.CharField(max_length=51200)                      # 研究成果
    promotional_video_url = models.CharField(max_length=1024)                       # 宣传视频 URL

    picture_128px = ImageSpecField(                                                 # 头像标准大小
        source="picture",
        processors=[ResizeToFill(128, 128)],    # 处理后的图像大小
        format='JPEG',                          # 处理后的图片格式
        options={'quality': 95}                 # 处理后的图片质量
    )


class Student(models.Model):
    GENDER_CHOICES = [('M', 'male'), ('F', 'female'), ('U', 'unknown')]
    AUTH_STATE_CHOICES = [('UQ', 'unqualified'), ('QD', 'qualified')]
    DEGREE_CHOICES = [('UG', 'undergraduate'), ('MT', 'master'), ('DT', 'doctor')]

    student_id = models.AutoField(primary_key=True)                                 # 学生 ID
    user = models.OneToOneField(User, on_delete=models.CASCADE)                     # 用户账户
    follows = models.ManyToManyField(User, related_name='student_fans')             # 关注关系

    account = models.CharField(max_length=32, null=False, unique=True)              # 账号
    password = models.CharField(max_length=32, null=False)                          # 密码
    name = models.CharField(max_length=16, null=False)                              # 名称
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')    # 性别
    school = models.CharField(max_length=32)                                        # 学校
    department = models.CharField(max_length=32)                                    # 院系
    major = models.CharField(max_length=32)                                         # 专业
    degree = models.CharField(max_length=2, choices=DEGREE_CHOICES, default='UG')   # 学位
    auth_state = models.CharField(max_length=2, choices=AUTH_STATE_CHOICES, default='UQ')  # 认证状态

    picture = models.ImageField(upload_to=custom_upload_path)                       # 头像
    signature = models.CharField(max_length=1024)                                   # 签名
    phone = models.CharField(max_length=64)                                         # 电话
    email = models.CharField(max_length=64)                                         # 邮箱
    homepage = models.CharField(max_length=128)                                     # 主页
    address = models.CharField(max_length=128)                                      # 地址
    student_number = models.CharField(max_length=32)                                # 学号
    id_number = models.CharField(max_length=32)                                     # 身份证号
    introduction = models.CharField(max_length=51200)                               # 个人介绍
    research_interest = models.CharField(max_length=51200)                          # 研究兴趣
    research_experience = models.CharField(max_length=51200)                        # 研究经历
    promotional_video_url = models.CharField(max_length=1024)                       # 宣传视频 URL

    picture_128px = ImageSpecField(                                                 # 头像标准大小
        source="picture",
        processors=[ResizeToFill(128, 128)],    # 处理后的图像大小
        format='JPEG',                          # 处理后的图片格式
        options={'quality': 95}                 # 处理后的图片质量
    )