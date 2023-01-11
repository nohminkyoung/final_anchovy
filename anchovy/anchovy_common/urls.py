from django.urls import path
from django.contrib.auth import views as auth_views
from . import views #현재 폴더에서 views를 가리킨다.


urlpatterns = [
    path('', views.make_login, name='login'), # 로그인을 기본경로로(ip만이용)
    path('anchovy_common/signup/', views.signup),
    path('tutorial/', views.tutorial,name='tutorial'),
    path('duplication/', views.duplication,name='duplication'),
]

