from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from anchovy_common.models import Custom_User, User_status
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


def settings(request):
    return render(request, 'anchovy_settings/settings.html')

def nickname(request):
    log_user = Custom_User.objects.get(username=request.user)
    data = request.POST.get('newnickname')
    errMsg = {}

    if data != None:
        if data == '':
            errMsg['error'] = '닉네임을 입력해주세요'
        elif ' ' in data:
            errMsg['error'] = '닉네임은 공백을 포함할 수 없습니다'
        else:
            log_user.nickname = data
            log_user.save()
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