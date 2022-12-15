from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from anchovy_common.forms import UserForm
from django.http import HttpResponseRedirect

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            # login(request, user)  # 로그인
            return redirect('login')
    else:
        form = UserForm()
    return render(request, 'anchovy_common/signup.html',{'form': form})


def tutorial(request):
    return render(request, 'anchovy_common/tutorial.html')