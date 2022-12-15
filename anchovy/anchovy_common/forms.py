from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Custom_User


class UserForm(UserCreationForm):
    nickname = forms.CharField(label = "닉네임")
    class Meta:
        model = Custom_User
        fields = ("username", "password1", "password2", 'nickname')
