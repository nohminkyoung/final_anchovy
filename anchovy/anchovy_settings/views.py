from django.shortcuts import render

def settings(request):
    return render(request, 'anchovy_settings/settings.html')

def nickname(request):
    return render(request, 'anchovy_settings/nickname.html')
    
def people(request):
    return render(request, 'anchovy_settings/people.html')

def logout(request):
    return render(request, 'anchovy_settings/logout.html')

def quit(request):
    return render(request, 'anchovy_settings/quit.html')

