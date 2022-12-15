from django.shortcuts import render

def index(request):
    return render(request, 'anchovy_train/train.html')

def choice(request):
    return render(request, 'anchovy_train/train_choice.html')

def train_result(request):
    return render(request, 'anchovy_train/train_result.html')

def train_train(request):
    return render(request, 'anchovy_train/train_train.html')

def train_practice(request):
    return render(request, 'anchovy_train/train_practice.html')