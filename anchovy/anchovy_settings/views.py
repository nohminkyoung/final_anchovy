from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from anchovy_common.models import Custom_User


def settings(request):
    return render(request, 'anchovy_settings/settings.html')

def nickname(request):
    log_user = Custom_User.objects.get(username=request.user)
    data = request.POST.get('newnickname')
    errMsg = {'error_before':''}
    check ={}
    if data != None:
        if data == '':
            errMsg['error'] = '닉네임을 입력해주세요'
        elif ' ' in data:
            errMsg['error'] = '닉네임은 공백을 포함할 수 없습니다'
        else:
            log_user.nickname = data
            log_user.save()
            return render(request, 'anchovy_main/index.html')
    
    return render(request, 'anchovy_settings/nickname.html',{'errMsg':errMsg})
    
    
def people(request):
    return render(request, 'anchovy_settings/people.html')

def quit(request):
    return render(request, 'anchovy_settings/quit.html')


def make_logout(request):
    logout(request)
    return redirect('login')
