from django.db import models
from anchovy_common.models import Custom_User
# Create your models here.

class Train(models.Model):
    author = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, verbose_name = '유저 아아디')
    train_date = models.DateField(verbose_name = '운동 날짜')
    train_time = models.TimeField(verbose_name = '운동 시간')
    train_kind =  models.IntegerField(verbose_name = '운동 종류')
    train_set = models.IntegerField(verbose_name = '운동 세트',null=True)
    train_all_count = models.IntegerField(verbose_name = '운동 1세트당 횟수',null=True)
    train_accurate_count = models.IntegerField(verbose_name = '정확하게한 횟수',null=True)
    train_rest = models.IntegerField(verbose_name = '휴식시간',null=True)
        
    