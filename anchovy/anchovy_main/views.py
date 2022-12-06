from django.shortcuts import render

def index(request):
    return render(request, 'anchovy_common/login.html')