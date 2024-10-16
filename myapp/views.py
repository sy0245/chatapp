from django.shortcuts import redirect, render, get_object_or_404
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate
from .forms import Signupform,Talkroom,UsernameChangeForm,MailChangeForm,IconChangeForm,PasswordChangeForm
from .forms import Loginform

from django.views import generic 
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordChangeDoneView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser, Message
from django.contrib.auth.decorators import login_required
from django.db.models import Q,Case, When, Value, IntegerField
import operator


def index(request):
    return render(request, "myapp/index.html")

# def signup_view(request):
#     if request.method == 'POST':
#         form = Signupform(request.POST,request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#         else:
#             return render(request, "myapp/signup.html", {'form': form})
#     else:
#         form = Signupform()
#         return render(request, "myapp/signup.html", {'form': form})

# class SignupView(generic.FormView):
#     template_name="signup.html"
#     form_class=Signupform
#     success_url=reverse_lazy("index")

#     def form_valid(self,form):
#         form.send_email()
#         return super().form_valid(form)

# def login_view(request):
#     if request.method == 'POST':
#         form = Loginform(request, request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('friends')
#                 else:
#                     form.add_error(None, 'アカウントが無効です。')
#                     return render(request, 'myapp/login.html', {'form': form})
#             else:
#                 form.add_error(None, 'ユーザー名またはパスワードが間違っています。')
#                 return render(request, 'myapp/login.html', {'form': form})
#         else:
#             return render(request, 'myapp/login.html', {'form': form})
#     if request.method == 'GET':
#         form = Loginform(request)
#         return render(request, 'myapp/login.html', {'form': form})
    
@login_required
def friends(request):
    info = []
    info_have_message = []
    info_have_no_message = []
    user = request.user
    query = request.GET.get('query')
    if query:
            friends = CustomUser.objects.filter(username__icontains=query).exclude(id=user.id)
    else:
        friends = CustomUser.objects.exclude(id=user.id)
        # トーク情報とフレンド情報を含む info を作成
    for friend in friends:
        # 最新のメッセージの取得
        latest_message = Message.objects.filter(Q(sendername=user,recipientname=friend) | Q(recipientname=user, sendername=friend)
        ).order_by('timestamp').last()
        if latest_message:
            info_have_message.append([friend, latest_message.content, CustomUser.objects.get(username=friend).picture,latest_message.timestamp])
        else:
            info_have_no_message.append([friend, "",CustomUser.objects.get(username=friend).picture ,""])
        # 時間順に並び替え
    info_have_message = sorted(info_have_message, key=operator.itemgetter(2), reverse=True)
    info.extend(info_have_message)
    info.extend(info_have_no_message)
    context = {"info": info}
    return render(request, "myapp/friends.html", context)

@login_required
def talk_room(request,user_id):
    user=request.user
    talk_aite=get_object_or_404(CustomUser, id=user_id)
    messages=Message.objects.filter(Q(sendername=user,recipientname=talk_aite) | Q(recipientname=user, sendername=talk_aite)).order_by('timestamp')
    
    form=Talkroom()
    context_talkroom={
        "talk_aite":talk_aite,
        "messages":messages,
        "form":form
    }
    if request.method == 'POST':
        new_message=Message(sendername=user,recipientname=talk_aite)
        form=Talkroom(request.POST,instance=new_message)
        if form.is_valid():
            form.save()
            return redirect('talk_room',user_id)
        else:
            form.add_error(None, 'もう一度メッセージを送ってください。')
            return render(request,'myapp/talk_room.html',context_talkroom)
    
    else:
        return render(request,'myapp/talk_room.html',context_talkroom)
@login_required    
def setting(request):
    return render(request, "myapp/setting.html")

@login_required
def username_change(request):
    user=request.user
    form=UsernameChangeForm(instance=user)
    context={
        "form":form
    }
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('username_change_done')
        else:
            form.add_error(None, 'もう一度新しいユーザー名を入力してください。')
            return render(request, "myapp/username_change.html",context)
    else:
        return render(request, "myapp/username_change.html",context)
@login_required
def username_change_done(request):
    return render(request, "myapp/username_change_done.html")

@login_required
def mail_change(request):
    user=request.user
    form=MailChangeForm(instance=user)
    context={
        "form":form
    }
    if request.method == 'POST':
        form = MailChangeForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('mail_change_done')
        else:
            form.add_error(None, 'もう一度新しいメールアドレスを入力してください。')
            return render(request, "myapp/mail_change.html",context)
    else:
        return render(request, "myapp/mail_change.html",context)
@login_required
def mail_change_done(request):
    return render(request, "myapp/mail_change_done.html")
@login_required             
def icon_change(request):
    user=request.user
    form=IconChangeForm(instance=user)
    context={
        "form":form
    }
    if request.method == 'POST':
        form = IconChangeForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('icon_change_done')
        else:
            form.add_error(None, 'もう一度新しい写真を入力してください。')
            return render(request, "myapp/icon_change.html",context)
    else:
        return render(request, "myapp/icon_change.html",context)
@login_required
def icon_change_done(request):
    return render(request, "myapp/icon_change_done.html")


class Password_Change(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("password_change_done")
    template_name = "myapp/password_change.html"


class Password_Chang_Done(PasswordChangeDoneView):
    template_name = "myapp/password_change_done.html"

class Logout(LoginRequiredMixin,LogoutView):
    template_name= "myapp/logout.html"
    next_page= "index"