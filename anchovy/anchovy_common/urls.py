from django.urls import path
from django.contrib.auth import views as auth_views
from . import views #현재 폴더에서 views를 가리킨다.

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='anchovy_common/login.html'
    ), name='login'),
    path('signup', views.signup),
    path('tutorial/', views.tutorial),
]

