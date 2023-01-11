from django.contrib import admin
from django.urls import path
from . import views #현재 폴더에서 views를 가리킨다.


urlpatterns = [
    path('', views.index, name = 'train'),
    
    path('choice_squat/',views.choice_squat, name='choice_squat'),
    path('choice_push_up/',views.choice_push_up, name='choice_push_up'),
    path('make_set',views.make_set, name='make_set'),
    
    path('train_choice/', views.choice, name = 'choice'),
    
    path('push_up', views.push_up, name='push_up'),
    path('squat',views.squat, name='squat'),
    
    path('train_choice/train_squat/', views.train_squat, name='train_squat'),
    path('train_choice/train_pushup/', views.train_pushup, name='train_pushup'),
    
    path('add_database', views.add_database, name='add_database'),
    
    path('train_choice/train_train/train_result/', views.train_result, name='train_result'),
    
    path('back_kind/', views.back_kind, name='back_kind'),
    path('stop', views.stop, name='stop')
    
    
    



]
