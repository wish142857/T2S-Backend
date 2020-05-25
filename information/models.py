from django.db import models
from user.models import Teacher, Student


class Information(models.Model):
    RECEIVER_TYPE = [('T', 'teacher'), ('S', 'student')]
    INFORMATION_TYPE = [('T', 'txt'), ('P', 'picture')]
    INFORMATION_STATE = [('N', 'new'), ('R', 'read'), ('H', 'hide')]

    information_id = models.AutoField(primary_key=True)         # 消息 ID
    receiver_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # 接收老师
    receiver_student = models.ForeignKey(Student, on_delete=models.CASCADE)  # 接收学生

    receiver_type = models.CharField(                           # 接受者类型
        max_length=1, choices=RECEIVER_TYPE, default='T')
    information_type = models.CharField(                        # 消息类型
        max_length=1, choices=INFORMATION_TYPE, default='T')
    information_content = models.BinaryField()                  # 消息内容
    information_time = models.DateTimeField(auto_now_add=True)  # 消息时间
    information_state = models.CharField(                       # 消息状态
        max_length=1, choices=INFORMATION_STATE, default='N')
