from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Person(User):
    user_name = models.CharField(max_length=32, verbose_name = '유저 닉네임') # 닉네임 추가  
    
    
class User_info(models.Model):
    user_id = models.CharField(max_length=32, unique = True, verbose_name = '유저 아이디') # 아이디는 15자 이내로
    user_name = models.CharField(max_length=32, verbose_name = '유저 닉네임') # 비밀번호는 8~15자 
    