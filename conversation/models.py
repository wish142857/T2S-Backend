from django.db import models
from django.contrib.auth.models import User
from user.models import Teacher, Student


class Message(models.Model):
    SENDER_TYPE_CHOICES = [('T', 'teacher'), ('S', 'student')]
    RECEIVER_TYPE_CHOICES = [('T', 'teacher'), ('S', 'student')]
    MESSAGE_TYPE_CHOICES = [('T', 'txt'), ('P', 'picture')]

    message_id = models.AutoField(primary_key=True)             # 消息 ID
    sender_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, related_name='s_messages')    # 发送老师
    sender_student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, related_name='s_messages')    # 发送学生
    receiver_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, related_name='r_messages')  # 接收老师
    receiver_student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, related_name='r_messages')  # 接收学生

    sender_type = models.CharField(                             # 发送者类型
        max_length=1, choices=SENDER_TYPE_CHOICES, null=False)
    receiver_type = models.CharField(                           # 接收者类型
        max_length=1, choices=RECEIVER_TYPE_CHOICES, null=False)
    message_type = models.CharField(                            # 消息类型
        max_length=1, choices=MESSAGE_TYPE_CHOICES, default='T')
    message_content = models.BinaryField()                      # 消息内容
    message_time = models.DateTimeField(auto_now_add=True)      # 消息时间
