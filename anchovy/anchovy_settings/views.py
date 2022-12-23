from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from anchovy_common.models import Custom_User, User_status, battle
from anchovy_user.models import Friend
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


def settings(request):
    return render(request, 'anchovy_settings/settings.html')

def nickname(request):
    log_user = Custom_User.objects.get(username=request.user)
    log_user_status = User_status.objects.get(username=request.user)
    log_user_freind = Friend.objects.filter(friend_name=request.user)
    log_user_lose = battle.objects.filter(lose_username=request.user)
    log_user_earn = battle.objects.filter(earn_username=request.user)
    
    data = request.POST.get('newnickname')
    errMsg = {}

    if data != None:
        if data == '':
            errMsg['error'] = '닉네임을 입력해주세요'
        elif ' ' in data:
            errMsg['error'] = '닉네임은 공백을 포함할 수 없습니다'
        else:
            log_user.nickname = data #custom_user의 닉네임 변경
            log_user.save()
            log_user_status.nickname = data # user_status의 닉네임 변경
            log_user_status.save()
            
            # 친구목록에 있는 닉네임 변경
            for freind in log_user_freind:
                print(freind)
                freind.friend_nickname = data 
                freind.save()
                
            # 베틀의 잃은 사람에 있는 닉네임 변경   
            for lose in log_user_lose:
                lose.lose_nickname = data 
                lose.save()
            
            # 베틀의 공격한 사람에 있는 닉네임 변경
            for lose in log_user_earn:
                lose.earn_nickname = data 
                lose.save()
        
            return redirect('main')
    
    return render(request, 'anchovy_settings/nickname.html',{'errMsg':errMsg})
    
    
def people(request):
    return render(request, 'anchovy_settings/people.html')

def quit(request):
    return render(request, 'anchovy_settings/quit.html')


def make_logout(request):
    logout(request)
    return redirect('login')


def delete(request):
    user_info = Custom_User.objects.get(username = request.user)
    logout(request) 
    user_info.delete()
    return render(request, 'anchovy_common/login3.html')