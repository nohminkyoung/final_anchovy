from django.shortcuts import render
from anchovy_common.models import Custom_User, User_status

def index(request):
    return render(request, 'anchovy_main/index.html', {'user':Custom_User, 'status': User_status})

def cal(request):
    return render(request, 'anchovy_main/view.html')