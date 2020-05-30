from django.db import models
from user.models import Teacher, Student


class Information(models.Model):
    RECEIVER_TYPE_CHOICES = [('T', 'teacher'), ('S', 'student')]
    INFORMATION_TYPE_CHOICES = [('T', 'txt'), ('P', 'picture')]
    INFORMATION_STATE_CHOICES = [('N', 'new'), ('R', 'read'), ('H', 'hide')]

    information_id = models.AutoField(primary_key=True)         # 信息 ID
    receiver_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)  # 接收老师
    receiver_student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)  # 接收学生

    receiver_type = models.CharField(                           # 接受者类型
        max_length=1, choices=RECEIVER_TYPE_CHOICES, null=False)
    information_type = models.CharField(                        # 信息类型
        max_length=1, choices=INFORMATION_TYPE_CHOICES, default='T')
    information_state = models.CharField(                       # 信息状态
        max_length=1, choices=INFORMATION_STATE_CHOICES, default='N')
    information_content = models.BinaryField()                  # 信息内容
    information_time = models.DateTimeField(auto_now_add=True)  # 信息时间

