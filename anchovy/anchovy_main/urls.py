from django.contrib import admin
from django.urls import path
from . import views #현재 폴더에서 views를 가리킨다.


urlpatterns = [
    path('main/', views.index, name='main'),
    path('view/', views.cal),
]
