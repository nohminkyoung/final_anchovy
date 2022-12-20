from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from anchovy_common.models import Custom_User


def settings(request):
    return render(request, 'anchovy_settings/settings.html')

def nickname(request):
    log_user = Custom_User.objects.get(username=request.user)
    
    data = request.POST.get('newnickname')
    print(data)
    
    log_user.nickname = data
    log_user.save()
    
    return render(request, 'anchovy_settings/nickname.html')
    
def people(request):
    return render(request, 'anchovy_settings/people.html')

def quit(request):
    return render(request, 'anchovy_settings/quit.html')


def make_logout(request):
    logout(request)
    return redirect('login')
