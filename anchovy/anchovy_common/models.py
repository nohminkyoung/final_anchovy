from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Custom_User(AbstractUser):
    nickname = models.CharField(max_length=150, verbose_name = '유저 닉네임',default = '') # 닉네임 추가  
    
class User_status(models.Model):
    author = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, verbose_name = '유저 아아디')
    nickname = models.CharField(max_length=150, verbose_name = '유저 닉네임',default = '')
    protein = models.IntegerField(verbose_name = '유저 프로틴레벨')
    coupon = models.IntegerField(verbose_name = '유저 쿠폰')
    recent_date = models.DateField(verbose_name = '최근 운동 날짜')
    recent_time = models.TimeField(verbose_name = '최근 운동 시간')
    character_lv = models.IntegerField(verbose_name = '유저 현재 캐릭터')
    week_train_count = models.IntegerField(verbose_name = '1주일간 운동 횟수')


class battle(models.Model):
    author = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    lose_username = models.CharField(max_length=150, verbose_name = '뺏긴사람 아이디')
    lose_nickname = models.CharField(max_length=150, verbose_name = '뺏긴사람 닉네임')
    earn_username = models.CharField(max_length=150, verbose_name = '뺏은사람 아이디')
    earn_nickname = models.CharField(max_length=150, verbose_name = '뺏은사람 닉네임')
    lose_date = models.DateField(verbose_name = '뺏긴 날짜')
    lose_time = models.TimeField(verbose_name = '뻇긴 시간')
