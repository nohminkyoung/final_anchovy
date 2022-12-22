from django.db import models
from anchovy_common.models import Custom_User

# Create your models here.

class Friend(models.Model):
    author = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    fd = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, verbose_name = '유저 아아디')
    friend_name = models.CharField(max_length=150, verbose_name = '유저의 친구 아아디')
    friend_nickname = models.CharField(max_length=150, verbose_name = '유저 친구 닉네임',default = '')
    friend_protein = models.IntegerField(verbose_name = '유저 친구 프로틴레벨')
    