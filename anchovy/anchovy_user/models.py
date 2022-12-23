from django.db import models
from anchovy_common.models import Custom_User,User_status

# Create your models here.

class Friend(models.Model):
    author = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    # fd = models.ForeignKey(User_status, on_delete=models.CASCADE)  # 외래키 이걸로 연결
    username = models.CharField(max_length=150, verbose_name = '유저 아아디')
    friend_name = models.CharField(max_length=150, verbose_name = '유저의 친구 아아디')
    friend_nickname = models.CharField(max_length=150, verbose_name = '유저 친구 닉네임',default = '')
    friend_protein = models.IntegerField(verbose_name = '유저 친구 프로틴레벨')
    # friend_lv = models.IntegerField(verbose_name = '유저 친구 캐릭터') # 친구 캐릭레벨 추가하기 (add friend 에 추가 )
    