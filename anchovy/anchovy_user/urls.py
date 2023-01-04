from django.contrib import admin
from django.urls import path
from . import views #현재 폴더에서 views를 가리킨다.

urlpatterns = [
    path('', views.index),
    path('friend_add/', views.add),
    path('fd_add/', views.fd_add, name='fd_add'),
    path('friend_detail/<str:user_name>/', views.detail, name ='detail'),
    path('new_steal', views.new_steal, name='new_steal'),
    path('btn_add',views.btn_add, name='btn_add')
]
