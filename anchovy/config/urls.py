"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('anchovy_common/', include('anchovy_common.urls')),
    path('anchovy_main/', include('anchovy_main.urls')),
    path('anchovy_notice/', include('anchovy_notice.urls')),
    path('anchovy_settings/', include('anchovy_settings.urls')),
    path('anchovy_train/', include('anchovy_train.urls')),
    path('anchovy_user/', include('anchovy_user.urls')),

]
