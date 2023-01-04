from django.shortcuts import render
from anchovy_train.models import Train
from datetime import datetime

# 각도 계산을 위해 import
from django.http import HttpResponse 
from django.http import StreamingHttpResponse
import json


def index(request):
    return render(request, 'anchovy_train/train.html')

def choice(request):
    return render(request, 'anchovy_train/train_choice.html')

def train_result(request):
    login_user = request.user # 로그인 유저
    now = datetime.now() # 현재 날짜 가져오기 위함
    
    # 로그인정보가 같고, 오늘 날짜와 같은 데이터 불러오기
    train_data = Train.objects.filter(username=login_user).filter(train_date=now.date()) 
    train_time_sort = train_data.order_by('-train_time').values() # 최근순으로 정력
    
    
    # 가장 최근 데이터를 set의 값에 따라 가져오도록 만들기 위함 (3세트 하면 3개의 연속된 데이터)
    data_list = []
    for i in range(train_time_sort[0]['train_set']): # 세트 수 만큼 반복
        data_list.append(train_time_sort[i]) # 세트 수에 맞는 데이터들만 가져오기

    all_score = 0
    accurate_score = 0
    for i,data in enumerate(data_list):
        data['set'] = i+1 # 몇번째 세트수인지
        all_score += data['train_all_count'] # 만점일 경우의 점수 
        accurate_score += data['train_accurate_count'] # 정확하게 한 점수
        
    kind = data_list[0]['train_kind'] # 운동 종류 뽑기
    persent = round((accurate_score/all_score)*100) # 몇 퍼센트 달성인지
    
    return render(request, 'anchovy_train/train_result.html',
                  {'data_list':data_list,'all_score':all_score,'accurate_score':accurate_score,'persent':persent,'kind':kind})
    

def train_train(request):
    return render(request, 'anchovy_train/train_train.html')

def train_practice(request):
    return render(request, 'anchovy_train/train_practice.html')

def test(request):
    return render(request, 'anchovy_train/test.html')

def angle_cal(request):
    
    x = request.GET.get('x')
    y = request.GET.get('y')
    z = request.GET.get('z')
    
        