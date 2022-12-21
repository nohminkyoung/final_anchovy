from django.contrib import admin
from django.urls import path
from . import views #현재 폴더에서 views를 가리킨다.


urlpatterns = [
    path('settings/',views.settings),
    path('nickname/', views.nickname),
    path('people/', views.people),
    path('logout/', views.make_logout, name='logout'),
    path('quit/', views.quit),
    path('delete', views.delete, name='delete')
]

