from django.shortcuts import render,redirect
from .models import Notice
from anchovy_common.models import battle, User_status
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def index(request):
    now = datetime.now() # 현재 
    time = now - relativedelta(months=1) # 한달 전
    dic = {'today': now.date()}
    
    Notice_data = Notice.objects.filter(username=request.user).filter(notice_date__gte=time.date()).order_by('-notice_date' ,'-notice_time').values()
    battle_data = battle.objects.filter(username=request.user).filter(lose_date__gte=time.date()).order_by('-lose_date' , '-lose_time').values()
    
    check = len(list(Notice_data))
    
    if check != 0:
        prev = Notice_data[0]
        for notice in Notice_data:
            
            notice['no_time'] = int(now.strftime('%H')) - int(notice['notice_time'].strftime('%H'))
            notice['no_min'] = int(now.strftime('%M')) - int(notice['notice_time'].strftime('%M'))
            
            # 디비의 첫번째 데이터의 날짜만 출력(기준)
            if prev == notice:
                notice['check'] = 1
                continue
            
            #이미 출력된 날짜와 같은 날짜면 날짜가 안나오게 하기위해서 0으로 
            if notice['notice_date'] == prev['notice_date']:
                notice['check'] = 0
            
            # 새로운 날짜가 등장하면 출력되게 해주기 위해서 
            else:
                notice['check'] = 1

            prev = notice 
        
        for notice in Notice_data:
            # 프로틴 상승(뺏음)
            if notice['notice_status'] == 2:
                for battle_value in battle_data:
                    if notice['notice_time'] == battle_value['lose_time'] and notice['notice_date'] == battle_value['lose_date']:
                        if battle_value['username'] == battle_value['earn_username']:
                            notice['battle_user'] = battle_value['lose_nickname']
                        
            # 프로틴 하강(뺏김)
            elif notice['notice_status'] == 3:
                for battle_value in battle_data:
                    if notice['notice_time'] == battle_value['lose_time'] and notice['notice_date'] == battle_value['lose_date']:
                        if battle_value['username'] == battle_value['lose_username']:
                            notice['battle_user'] = battle_value['earn_nickname']
                            
            
    print(Notice_data)
    return render(request, 'anchovy_notice/notice.html',{'Notice':Notice_data, 'dic':dic,'check':check})


def make_notice(request):
    
    login_user = User_status.objects.get(username=request.user)
    now = datetime.now() # 현재 
    make_time = login_user.recent_date + timedelta(weeks=3) # 3주 후
    check_time = datetime.strptime(str(make_time)+' '+str(login_user.recent_time), '%Y-%m-%d %H:%M:%S')
    
    check_data = Notice.objects.filter(username=request.user).filter(notice_status=1).values()
    
    
    if len(list(check_data)) == 0:
        if check_time <= now:
            # status : 1-운동안한지 오래됨, 2-뺏음, 3- 뺏김
            status_data = Notice(notice_date=make_time, notice_time=login_user.recent_time,
                                username=login_user.username,notice_status=1, author_id=login_user.author_id)

            status_data.save()
            
            
    return redirect('notice')