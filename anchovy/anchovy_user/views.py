from django.shortcuts import render,redirect
from anchovy_common.models import User_status, Custom_User, battle
from anchovy_notice.models import Notice
from anchovy_user.models import Friend
from datetime import datetime, date, time
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

def index(request):
    # 내 정보 가져오기
    user = User_status.objects.get(username =request.user)

    # 랭킹 데이터 불러오기
    data_rank = User_status.objects.all().values() 
    sort_data = data_rank.order_by('-protein') #protein컬럼을 사용해서 내림차순 정렬
    
    # 공동순위를 위한 작업
    prev = sort_data[0]['protein']
    i = 1
    for idx,dd in enumerate(sort_data):
        
        if dd['protein'] == prev:
            dd['rank'] = i #data에 rank값 추가하는 법
                            #(for문을 돌려 한 딕셔너리씩 접근이 필요)
        else :
            i = idx+1
            dd['rank'] = i
            
        prev = dd['protein']

    # 친구데이터 불러오기
    friend= Friend.objects.filter(username =request.user).values() # 로그인 된 내 상태 request.user로 불러옴
    sort_fiend = friend.order_by('id')
    
    #html에 노출시킬 데이터
    return render(request, 'anchovy_user/user.html', {'sort_data':sort_data, 'sort_fiend':sort_fiend,'user':user} )


def detail(request, user_id): #user_id값을 같이 받아오기
    user = User_status.objects.get(author_id=user_id) # 고유한 id 값이 user_id와 같은 값만 불러오기
    
    target_user = Custom_User.objects.get(username=request.user) #로그인된 정보
    
    return render(request, 'anchovy_user/friend_detail.html', {'user':user, 'target_user':target_user})


@csrf_exempt 
def fd_add(request):
    user = User_status.objects.get(username =request.user)
    try:
        data = request.POST.get('id_values')
        Custom_User.objects.get(username = data)

    except Custom_User.DoesNotExist:
        status = 0
        return HttpResponse(json.dumps({'status':status}))
    
    else:
        try:
            Friend.objects.get(friend_name = data)
        
        # 친구 추가 할 수 있음
        except Friend.DoesNotExist:
            print('ddfdfs')
            fd_id = User_status.objects.get(username = data)
            status = 2
            status_data = Friend(username=user.username, friend_name=fd_id.username, 
                                friend_nickname = fd_id.nickname, friend_protein=fd_id.protein, author_id = user.author_id)
            status_data.save()
            return HttpResponse(json.dumps({'status':status}))
        
        else:
            status = 1
            return HttpResponse(json.dumps({'status':status}))
        
def add(request):
    return render(request, 'anchovy_user/friend_add.html')


@csrf_exempt 
def new_steal(request):
    if request.POST:
        user_id = request.POST.get('user_id')
        print(user_id)
        
        user = User_status.objects.get(author_id=user_id) # 고유한 id 값이 user_id와 같은 값만 불러오기(친구)
    
        target_user = User_status.objects.get(username=request.user) #로그인된 정보(나)
        
        
        if target_user.coupon < 1: # 쿠폰이 없을 때
            check = 2
        
        elif user.protein == 0 : # 상대의 프로틴이 0일 때 
            check =3
            
        elif target_user.coupon >= 1: # 쿠폰이 있을 때
            target_user.protein += 1
            user.protein -= 1
            target_user.coupon -= 1
            target_user.save()
            user.save()
            
            # 현재시간
            now = datetime.now()
            create_date = date(now.year, now.month, now.day)
            create_time = time(now.hour, now.minute, 0)
            # 베틀 데이터 추가
            status_data = battle(username = target_user.username, lose_username=user.username,lose_nickname=user.nickname,
                                earn_username=target_user.username, earn_nickname=target_user.nickname,
                                lose_date=create_date, lose_time=create_time,
                                author_id = target_user.author_id)
            status_data.save()

            # 알림 데이터 추가
            # status : 1-운동안한지 오래됨, 2-뺏음, 3- 뺏김
            
            # 뺏은 데이터
            status_data_steal = Notice(notice_date=create_date, notice_time=create_time,
                                username=target_user.username,notice_status=2, author_id=target_user.author_id)
            status_data_steal.save()
            
            # 뺏긴 데이터
            status_data_lose = Notice(notice_date=create_date, notice_time=create_time,
                                username=user.username,notice_status=3, author_id=user.author_id)
            status_data_lose.save()
            check = 1
            

    print(user.protein)

    return HttpResponse(json.dumps({'check':check}))