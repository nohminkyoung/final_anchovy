from django.shortcuts import render

def index(request):
    return render(request, 'anchovy_user/user.html')

def add(request):
    return render(request, 'anchovy_user/friend_add.html')

def detail(request):
    return render(request, 'anchovy_user/friend_detail.html')