from django.db import models
from django.contrib.auth.models import User
from user.models import Teacher, Student


class Message(models.Model):
    OWNER_TYPE_CHOICES = [('T', 'teacher'), ('S', 'student')]
    OBJECT_TYPE_CHOICES = [('T', 'teacher'), ('S', 'student')]
    MESSAGE_WAY_CHOICES = [('S', 'send'), ('R', 'receive')]
    MESSAGE_TYPE_CHOICES = [('T', 'txt'), ('P', 'picture')]

    message_id = models.AutoField(primary_key=True)             # 消息 ID
    owner_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='p_message')   # 所属老师
    owner_student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='p_message')   # 所属学生
    object_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='n_message')  # 对象老师
    object_student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='n_message')  # 对象学生

    owner_type = models.CharField(                              # 所有者类型
        max_length=1, choices=OWNER_TYPE_CHOICES, null=False)
    object_type = models.CharField(                             # 对象类型
        max_length=1, choices=OBJECT_TYPE_CHOICES, null=False)
    message_way = models.CharField(                             # 消息方式
        max_length=1, choices=MESSAGE_WAY_CHOICES, null=False)
    message_type = models.CharField(                            # 消息类型
        max_length=1, choices=MESSAGE_TYPE_CHOICES, default='T')
    message_content = models.BinaryField()                      # 消息内容
    message_time = models.DateTimeField(auto_now_add=True)      # 消息时间
