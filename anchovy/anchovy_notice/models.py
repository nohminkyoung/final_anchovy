from django.db import models
from anchovy_common.models import Custom_User

# Create your models here.

class Notice(models.Model):
    author = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    notice_date = models.DateField(verbose_name = '알림생성날짜')
    notice_time = models.TimeField(verbose_name = '알림생성시간')
    username = models.CharField(max_length=150, verbose_name = '유저 아아디')
    notice_status = models.IntegerField(verbose_name = '알림 종류')