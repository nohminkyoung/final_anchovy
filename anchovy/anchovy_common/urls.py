from django.urls import path
from django.contrib.auth import views as auth_views
from . import views #현재 폴더에서 views를 가리킨다.


urlpatterns = [
    path('login/', views.make_login, name='login'),
    path('signup', views.signup),
]

