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
    sort_data = data_rank.order_by('-protein','-character_lv') #protein컬럼을 사용해서 내림차순 정렬
    
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


def detail(request, user_name): #user_id값을 같이 받아오기
    user = User_status.objects.get(username=user_name) # 고유한 id 값이 user_id와 같은 값만 불러오기 (친구)
    
    target_user = Custom_User.objects.get(username=request.user) #로그인된 정보 (나)
    
    
    my_friend = Friend.objects.filter(username = request.user) # 내친구들
    
    if len(list(my_friend.filter(friend_name = user.username))) == 0 :
        icon = 0 # 흰색(친구가 아닐때)
    else :
        icon = 1 # 검정(친구일때)

    
    return render(request, 'anchovy_user/friend_detail.html', {'user':user, 'target_user':target_user, 'icon':icon})


@csrf_exempt 
def fd_add(request):
    user = User_status.objects.get(username = request.user) 
    data = request.POST.get('id_values')
    
    user = User_status.objects.get(username = request.user) # 나
    my_friend = Friend.objects.filter(username = data) # 내친구들
    data = request.POST.get('friend_name') # 추가할 친구 아이디
    
    if str(request.user) != data :
        try: # 사용자 중 아이디가 존재하는지
            Custom_User.objects.get(username = data)

        except Custom_User.DoesNotExist: # 존재하지 않음
            status = 0
            return HttpResponse(json.dumps({'status':status}))
        
        else: # 존재 함
            try: # 내 친구목록에 없는지 확인
                Friend.objects.get(username=request.user,friend_name = data)
            
            # 친구 추가 할 수 있음
            except Friend.DoesNotExist: # 내친구에 그 아이디가 없을 때 
                fd_id = User_status.objects.get(username = data)
                status = 2
                status_data = Friend(username=user.username, friend_name=fd_id.username, 
                                    friend_nickname = fd_id.nickname, friend_protein=fd_id.protein, author_id = user.author_id) # friend_lv 추가하기 friend_lv=fd_id.character_lv
                status_data.save()
                return HttpResponse(json.dumps({'status':status}))
            
            else: # 내 친구에 그 아이디가 있을 때
                status = 1
                return HttpResponse(json.dumps({'status':status}))
    else : 
        status = 3
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
            status_data1 = battle(username = target_user.username, lose_username=user.username,lose_nickname=user.nickname,
                                earn_username=target_user.username, earn_nickname=target_user.nickname,
                                lose_date=create_date, lose_time=create_time,
                                author_id = target_user.author_id)
            status_data1.save()
            
            status_data2 = battle(username = user.username, lose_username=target_user.username,lose_nickname=target_user.nickname,
                                earn_username=user.username, earn_nickname=user.nickname,
                                lose_date=create_date, lose_time=create_time,
                                author_id = user.author_id)
            status_data2.save()

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


@csrf_exempt 
def btn_add(request):
    user = User_status.objects.get(username = request.user) # 나
    data = request.POST.get('friend_name') # 추가할 친구 아이디
    my_friend = Friend.objects.filter(username = request.user) # 내친구들
    fd = User_status.objects.get(username = data) # 친구가 될 사람의 정보
    print('ajshdfkahsdlkfhalskdfhalsdkfh',data)
    
    if data != None : 
        if len(list(my_friend.filter(friend_name = data))) == 0 : # 친구가 아니라 추가하기 
            
            icon_status = 0 # 친구가 없는 사람이라서 추가함 / 흰색 -> 검정
            
            status_data = Friend(username=user.username, friend_name=data, 
                                    friend_nickname = fd.nickname, friend_protein=fd.protein, author_id = user.author_id)
            status_data.save()
            
        else :
            del_data = Friend.objects.filter(username = request.user, friend_name = data)
            del_data.delete()
            
            icon_status = 1 # 삭제를 함 / 검정 -> 흰색
            
    return HttpResponse(json.dumps({'icon_status':icon_status}))
        
    