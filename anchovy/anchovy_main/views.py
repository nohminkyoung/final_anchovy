from django.shortcuts import render

def index(request):
    return render(request, 'anchovy_main/index.html')