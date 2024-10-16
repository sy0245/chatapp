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
from allauth.account.forms import LoginForm,SignupForm,ResetPasswordKeyForm,ResetPasswordForm
import os
from django.core.mail import EmailMessage

class Signupform(SignupForm):
    User = get_user_model()
    picture=forms.ImageField()
    class Meta:
        model = CustomUser
        fields = ('username',  'email', 'password1', 'password2','picture' )
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['placeholder'] = field.label
        def signup(self,request,user):
            user.picture=self.cleaned_data["picture"]
            user.save()
            return user
    # def send_email(self):
    #     name=self.cleaned_data["username"]
    #     email=self.cleaned_data["email"]
        
    #     subject="会員登録"
    #     message="送信者：{0}\nメールアドレス：{1}".format(name,email)
    #     from_email=os.environ.get("FROM_EMAIL")
    #     to_list=[os.environ.get("FROM_EMAIL")]
    #     cc_list=[email]

    #     message=EmailMessage(subject=subject,body=message,from_email=from_email,to=to_list,cc=cc_list)
    #     message.send()


class Loginform(LoginForm):
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

class MailChangeForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=("email",)
        labels={"email":"新しいメールアドレス"}
class IconChangeForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=("picture",)
    
class ResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ResetPassworKeydForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
