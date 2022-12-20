from django.shortcuts import render
from anchovy_common.models import User_status, Custom_User
from anchovy_user.models import Friend


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



def add(request):
    return render(request, 'anchovy_user/friend_add.html')



