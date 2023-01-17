from django.shortcuts import render
from anchovy_common.models import Custom_User, User_status, battle
from anchovy_train.models import Train
from anchovy_user.models import Friend
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse 
import time
from django.http import StreamingHttpResponse
from datetime import datetime, timedelta 


# index : Custom_User, User_status 참조 // 중앙 이미지 변경
def index(request):


    status_dic = {'lv':0, 'name':'', 'percent':0, 'recent_date':'', 'recent_ex':'', 'recent_score':0, 'goal':''}

    login_user = request.user

    #로그인 한 유저 닉네임 가져오기
    target_user = Custom_User.objects.get(username=login_user)
    #로그인 한 유저 Status 가져오기 
    target_status = User_status.objects.get(username=login_user)

    # 해골일 경우 일주일 안에 3번 운동 했을 경우 자동 멸치로 갱신
    if target_status.character_lv == 0 and target_status.week_train_count >= 3:
        target_status.character_lv = 1
        target_status.save()
    # ----------------------------------------------------- # 
    # Train Null 값 제거
    target_train = Train.objects.filter(username=login_user)
    for t_values in target_train:
        if (t_values.train_set == None) or (t_values.train_all_count == None) or (t_values.train_accurate_count == None):
            t_values.delete()
                
    # ----------------------------------------------------- # 
    # 프로틴 자동 갱신
    if target_status.protein >= 0 and target_status.protein <= 4:
        if target_status.character_lv == 1:
            pass
        elif target_status.character_lv == 0:
            pass
        else:
            target_status.character_lv = 1
            target_status.save()
    elif target_status.protein >= 5 and target_status.protein <= 11:
        if target_status.character_lv == 2:
            pass
        else:
            target_status.character_lv = 2
            target_status.save()
    elif target_status.protein >= 12 and target_status.protein <= 21:
        if target_status.character_lv == 3:
            pass
        else:
            target_status.character_lv = 3
            target_status.save()
    elif target_status.protein >= 22:
        if target_status.character_lv == 4:
            pass
        else:
            target_status.character_lv = 4
            target_status.save()
    # ------------------------------------#
    
    # 퍼센트 불러오기
    #print(target_training)
    target_weektrain = User_status.objects.get(username=target_user)
    status_dic = {'lv':0, 'name':'', 'percent':0, 'recent_date':'', 'recent_ex':0, 'recent_score':0, 'week_score':0}

    # 마지막 운동 기록
    try:
        target_recent = Train.objects.filter(username=target_user).last() # ID 값 기준 마지막 데이터 나옴
        target_ex = target_recent.train_kind # 최근 운동 종류
        target_date = target_recent.train_date
        target_set = target_recent.train_set
        re_date = target_date.strftime("%y/%m/%d") #최근 운동 날짜
        
        # 마지막 운동 전체 불러오기
        # 전체 운동 합계
        
        # 일주일 전까지 날짜 구하기
        today = datetime.now() # 오늘 날짜
        month30 = [2,4,6,9,11]
        month31 = [1,3,5,7,8,10,12]
        if today.strftime('%w') == '0': # 일요일 이였을 경우
            check_num = 6
        else:
            check_num = int((today - timedelta(days=1)).strftime('%w')) # 그외 요일이였을 경우
            
        # 마지막 날의 합산  
        #target_training = Train.objects.filter(username=target_user).filter(train_date = target_date).aggregate(Sum('train_accurate_count'))
        
        # 최근 마지막 운동 3세트 구하기
        target_recenttrain = Train.objects.filter(username=target_user).filter(train_date = target_date).filter(train_kind=target_ex).order_by('-id')
        
        for idx,recenttrain in enumerate(target_recenttrain):
            if idx == target_set:
                break
            status_dic['recent_score'] += recenttrain.train_accurate_count
            
        #####################################################################
        
        all_dates = Train.objects.filter(username=target_user).values()
        
        # 찾을 년월일 계산
        cal_day = int(today.strftime('%d')) - check_num
        cal_month = int(today.strftime('%m'))
        cal_year = int(today.strftime('%Y'))
        
        if cal_day < 1: #계산한 날짜가 1보다 작을경우
            cal_month = int(today.strftime('%m')) -1 #1보다 작았을 경우 월을 1줄인다.
            if int(today.strftime('%m')) in month30:
                cal_day+=30
            elif int(today.strftime('%m')) in month31:
                cal_day+=31
            else:
                cal_day+=28
            if cal_month < 1: # 해가 바뀌었을 경우 
                cal_year -=1
                
        for all_date in all_dates:
            check_day = int(all_date['train_date'].strftime('%d'))
            check_month = int(all_date['train_date'].strftime('%m'))
            check_year = int(all_date['train_date'].strftime('%Y'))
            if check_year >= cal_year and check_month >= cal_month :  
                if check_day >= cal_day:
                    status_dic['week_score'] += all_date['train_accurate_count']
                    
    
    except:
        status_dic['recent_ex'] = '없음'
        status_dic['goal'] = "목표 :일주일 이내 3번 운동하기"
        status_dic['percent'] = 0
    else:
        #최근 날짜 기록
        status_dic['recent_date'] = re_date
        
        # 최근 운동 기록
        if target_ex == 1:
            status_dic['recent_ex'] = '스쿼트'
        elif target_ex == 2:
            status_dic['recent_ex'] = '푸쉬업'
        
        # 최근 운동 정확한 점수 합계 and 변수 선언
        #status_dic['recent_score'] = target_training['train_accurate_count__sum']         
        
        # 목표 및 퍼센트 설정 하기
        if target_weektrain.protein == 0 and target_weektrain.character_lv == 0:
            max_value = '목표 :일주일 이내 3번 운동하기'
            status_dic['goal'] = max_value
            status_dic['percent'] = target_weektrain.week_train_count*33.3333333333333333
        elif target_weektrain.protein >= 0 and target_weektrain.protein <= 4:
            max_value = '목표 점수 : 120'
            status_dic['goal'] = max_value
            status_dic['percent'] = int(round(status_dic['week_score']/120, 2) * 100)
        elif target_weektrain.protein >= 5 and target_weektrain.protein <= 11:
            max_value = '목표 점수 : 150'
            status_dic['goal'] = max_value
            status_dic['percent'] = int(round(status_dic['week_score']/150, 2) * 100)
        elif target_weektrain.protein >= 12 and target_weektrain.protein <= 21:
            max_value = '목표 점수 : 180'
            status_dic['goal'] = max_value
            status_dic['percent'] = int(round(status_dic['week_score']/180, 2) * 100)
        elif target_weektrain.protein >= 22:
            max_value = '목표 점수 : 210'
            status_dic['goal'] = max_value
            status_dic['percent'] = int(round(status_dic['week_score']/210, 2) * 100)


    # ------------------------------------#
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
            
def coupon_active(request):
    if request.GET:
        login_user = request.user
        target_coupons = request.GET.get('coupons')
        friends = Friend.objects.filter(friend_name = login_user)

        # 쿠폰 사용
        if int(target_coupons) > 0:
            coupon_error = 0
            target_status = User_status.objects.get(username=login_user)
            target_status.coupon -= 1
            target_status.protein += 1
            target_status.save()
            
            for freind in friends : 
                freind.friend_protein += 1
                freind.save()
            
            
        else:
            coupon_error = 1
            
    return HttpResponse(json.dumps({'coupon_error': coupon_error }))


def stream(request):
    def event_stream():
        tmp_user = request.user
        tmp = User_status.objects.get(username=tmp_user) #처음 
        while True:
            # 정상 실행
            login_user = request.user
            if tmp_user == login_user:
                target_status = User_status.objects.get(username=login_user)
                # 중간에 프로틴이 변경이 되었다면
                if target_status.protein != tmp.protein:
                    ssm_status = '1'
                # 이상이 없는 경우
                else:
                    ssm_status = '0'
                yield 'data: %s\n\n' % ssm_status
            # 처음 들어왔을 때 등록되어 있는 로그인 유저와 다른 경우 상태값 2를 출력
            else:        
                ssm_status = '2'
                yield 'data: %s\n\n' % ssm_status
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')