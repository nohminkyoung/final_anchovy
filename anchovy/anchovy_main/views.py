from django.shortcuts import render
from anchovy_common.models import Custom_User, User_status, battle
from anchovy_train.models import Train
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse 
from datetime import datetime, date

# index : Custom_User, User_status 참조 // 중앙 이미지 변경
def index(request):

    status_dic = {'lv':0, 'name':''}

    login_user = request.user

    #로그인 한 유저 닉네임 가져오기
    target_user = Custom_User.objects.get(username=login_user)
    #로그인 한 유저 Status 가져오기 
    target_status = User_status.objects.get(username=login_user)

    ## 가져온 lv값에 따라 목표 점수 전달
    if target_status.character_lv == 0:
        status_dic['lv'] = 0
        status_dic['name'] = '뼈다귀'
    elif target_status.character_lv == 1:
        status_dic['lv'] = 1
        status_dic['name'] = '멸치'
    elif target_status.character_lv == 2:
        status_dic['lv'] = 2
        status_dic['name'] = '황새치'
    elif target_status.character_lv == 3:
        status_dic['goal'] = 180
        status_dic['lv'] = 3
        status_dic['name'] = '고등어'
    elif target_status.character_lv == 4:
        status_dic['lv'] = 4
        status_dic['name'] = '상어'

    context = {'log_user':target_user,'log_status':target_status, 'log_dic': status_dic }
    
    return render(request, 'anchovy_main/index.html', context)

@csrf_exempt
def cal(request):
    
    if request.POST:
        login_user = request.user
        T_data = []
        B_data = []
        year = request.POST.get('Year')
        month = request.POST.get('Month')
        Train_data = Train.objects.filter(username=login_user).filter(train_date__year=year,train_date__month=month)
        Battle_data = battle.objects.filter(username=login_user).filter(lose_date__year=year,lose_date__month=month)
        
        for i in Train_data:
            train_arr = {}
            train_arr['train_date'] = str(i.train_date)
            train_arr['train_kind'] = i.train_kind
            train_arr['train_set'] = i.train_set
            train_arr['train_all_count'] = i.train_all_count
            train_arr['train_accurate_count']= i.train_accurate_count
            T_data.append(train_arr)
        
        for j in Battle_data:
            battle_arr = {}
            battle_arr['username'] = j.username
            battle_arr['lose_username'] = j.lose_username
            battle_arr['earn_username'] = j.earn_username
            battle_arr['lose_date']= str(j.lose_date)
            battle_arr['lose_nickname'] = j.lose_nickname
            battle_arr['earn_nickname'] = j.earn_nickname
            B_data.append(battle_arr)
        

        return HttpResponse(json.dumps({'T_data':T_data, 'B_data':B_data}))

    return render(request, 'anchovy_main/view.html')

@csrf_exempt
def get_cal(request):
 
    if request.POST:
        login_user = request.user
        
        year = request.POST.get('Year')
        month = request.POST.get('Month')
        day = request.POST.get('Day')
                
        Train_data = Train.objects.filter(username=login_user).filter(train_date__year=year,train_date__month=month, train_date__day=day)
        Battle_data = battle.objects.filter(username=login_user).filter(lose_date__year=year,lose_date__month=month, lose_date__day=day)
        
        
        T_data = []
        B_data = []
        
        for i in Train_data:
            train_arr = {}
            train_arr['train_date'] = str(i.train_date)
            train_arr['train_kind'] = i.train_kind
            train_arr['train_set'] = i.train_set
            train_arr['train_all_count'] = i.train_all_count
            train_arr['train_accurate_count']= i.train_accurate_count
            T_data.append(train_arr)
            
        for j in Battle_data:
            battle_arr = {}
            battle_arr['username'] = j.username
            battle_arr['lose_username'] = j.lose_username
            battle_arr['earn_username'] = j.earn_username
            battle_arr['lose_date']= str(j.lose_date)
            battle_arr['lose_nickname'] = j.lose_nickname
            battle_arr['earn_nickname'] = j.earn_nickname
            B_data.append(battle_arr)
            
        return HttpResponse(json.dumps({'T_data':T_data, 'B_data':B_data}))
            
                        
@csrf_exempt 
def main_record(request):
    
    if request.POST:
        target_user = request.POST.get('user')
        target_user_lv = request.POST.get('lv')
        
        ## 최근 운동 기록 
        
        recent_data = []
        
        # --> 정확한 운동 점수 합산 (일주일 단위 추가해야 함)
        # --> training 값은 단일 값이 아니기 때문에 filter 사용
        target_training = Train.objects.filter(username=target_user).aggregate(Sum('train_accurate_count'))
        
        # --> 마지막 운동 기록
        target_recent = Train.objects.filter(username=target_user).last() 

        # -->최근 운동 기록 통합하기
        target_accurate_count = target_recent.train_accurate_count # 최근 운동 중 정확하게 한 운동
        target_date = target_recent.train_date
        re_date = target_date.strftime("%y/%m/%d")

        if target_recent.train_kind == 1:
            ex = '스쿼트'
        elif target_recent.train_kind == 2:
            ex = '푸쉬업'
        else:
            pass

        recent_record = {'date': re_date, 'count':target_accurate_count,'exercise':ex}

        
        ## 게이지 값 계산
        progress_data = []
        status_dic = {'percent':0}
        
        user_value = target_training['train_accurate_count__sum']
                
        if target_user_lv == '0':
            max_value = 0
        elif target_user_lv == '1':
            max_value = 120
        elif target_user_lv == '2':
            max_value = 150
        elif target_user_lv == '3':
            max_value = 180
        elif target_user_lv == '4':
            max_value = 210
        
        status_dic['percent'] = int(round(user_value/max_value, 2) * 100)

        recent_data.append(recent_record)
        progress_data.append(status_dic)
    
    return HttpResponse(json.dumps({'recent_data':recent_data, 'progress_data':progress_data}))