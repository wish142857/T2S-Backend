from django.db import models
from django.contrib.auth.models import User


class SearchRecord(models.Model):
    search_record_id = models.AutoField(primary_key=True)                   # 搜索记录 ID
    owner_user = models.ForeignKey(User, on_delete=models.CASCADE)          # 所属用户

    search_key = models.CharField(max_length=64)                            # 搜索关键字
    search_time = models.DateTimeField(auto_now_add=True)                   # 搜索时间
