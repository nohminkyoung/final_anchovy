from django.contrib import admin
from django.urls import path
from . import views #현재 폴더에서 views를 가리킨다.

urlpatterns = [
    path('', views.index),
    path('train_choice/', views.choice),
    path('train_choice/train_train/', views.train_train, name='train_train'),
    path('train_choice/train_practice/', views.train_practice, name='train_practice'),
    path('train_choice/train_train/train_result/', views.train_result, name='train_result'),
    path('test', views.test, name='test'),
    path('angle_cal', views.angle_cal, name='angle_cal'),
    
]