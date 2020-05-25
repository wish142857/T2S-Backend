from django.db import models
from user.models import Teacher, Student


class Recruitment(models.Model):
    RECRUITMENT_TYPE_CHOICES = [('UG', 'undergraduate'), ('MT', 'master'), ('DT', 'doctor')]
    INTENTION_STATE_CHOICES = [('O', 'ongoing'), ('S', 'succeed'), ('F', 'fail')]

    recruitment_id = models.AutoField(primary_key=True)                 # 招收意向 ID
    publisher = models.ForeignKey(Teacher, on_delete=models.CASCADE)    # 发布者

    recruitment_type = models.CharField(                                # 招收类型
        max_length=2, choices=RECRUITMENT_TYPE_CHOICES, default='UG')
    recruitment_number = models.IntegerField(null=False)                # 招收数量
    research_fields = models.CharField(max_length=51200)                # 研究方向
    introduction = models.CharField(max_length=51200)                   # 具体介绍
    intention_state = models.CharField(                                 # 意向状态
        max_length=1, choices=INTENTION_STATE_CHOICES, default='O')


class Application(models.Model):
    INTENTION_STATE_CHOICES = [('O', 'ongoing'), ('S', 'succeed'), ('F', 'fail')]

    application_id = models.AutoField(primary_key=True)                 # 申请意向 ID
    publisher = models.ForeignKey(Student, on_delete=models.CASCADE)    # 发布者

    research_interests = models.CharField(max_length=51200)             # 兴趣方向
    introduction = models.CharField(max_length=51200)                   # 个人简历
    intention_state = models.CharField(                                 # 意向状态
        max_length=1, choices=INTENTION_STATE_CHOICES, default='O')
