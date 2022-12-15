from django.shortcuts import render

def index(request):
    return render(request, 'anchovy_train/train.html')

def choice(request):
    return render(request, 'anchovy_train/train_choice.html')

def result(request):
    return render(request, 'anchovy_train/train_result.html')