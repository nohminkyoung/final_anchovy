from django.shortcuts import render

def index(request):
    return render(request, 'anchovy_settings/settings.html')

def tutorial(request):
    return render(request, 'anchovy_settings/tutorial.html')

def nickname(request):
    return render(request, 'anchovy_settings/nickname.html')
    
def people(request):
    return render(request, 'anchovy_settings/people.html')

def logout(request):
    return render(request, 'anchovy_settings/logout.html')

def quit(request):
    return render(request, 'anchovy_settings/quit.html')

