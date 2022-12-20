from django.contrib import admin
from django.urls import path
from . import views #현재 폴더에서 views를 가리킨다.


urlpatterns = [
    path('main/', views.index, name='main'),
    path('main_record/', views.main_record, name='main_record'),
    path('view/', views.cal, name='view'),
    path('get_cal/', views.get_cal, name='get_cal'),
    path('coupon_active/', views.coupon_active, name='coupon_active'),
    path('stream/', views.stream, name='stream')
    
]
