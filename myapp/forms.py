from typing import Any
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.forms.utils import ErrorDict
from .models import CustomUser,Message
from django import forms

class Signupform(UserCreationForm):
    User = get_user_model()

    class Meta:
        model = CustomUser
        fields = ('username',  'email', 'password1', 'password2','picture' )

class Loginform(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
             field.widget.attrs['placeholder'] = field.label

class Talkroom(forms.ModelForm):
    class Meta:
        model =Message
        fields = ('content',)

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username",)
        labels = {"username": "新しいユーザ名"}
class MailChangeForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=("email",)
        labels={"email":"新しいメールアドレス"}
class IconChangeForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=("picture",)
    
class PasswordChangeFrom(PasswordChangeForm):
    class Meta:
        model=CustomUser
        fields=("password",)