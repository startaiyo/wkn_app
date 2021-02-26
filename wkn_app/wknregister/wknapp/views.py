from django.shortcuts import render, redirect
import json
import sys # ErrorLog出力用
sys.path.append('/Users/startaiyo/opt/anaconda3/lib/python3.8/site-packages')
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm  # 追記
from django.contrib.auth import login
from django.urls import reverse_lazy
from . import forms

class MyLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = "wknapp/login.html"

class MyLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "wknapp/logout.html"

class IndexView(TemplateView):
    template_name = "wknapp/index.html"

class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "wknapp/create.html"
    success_url = reverse_lazy("login")

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
        
def index(request):
    context={'equipments':{"apple":"170","banana":"178"}}
    if request.method=="GET":
        return render(
            request,
            "wknapp/index.html",
            context
        )
    else:
        title = request.POST.get("title").split(',')
        many = request.POST.get("many")
        username=request.POST.get("username")
        title.append(many)
        title.append(username)
        print(title)
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

        #認証情報設定
        #ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
        credentials = ServiceAccountCredentials.from_json_keyfile_name('waken-order-9dc6a9680e5a.json', scope)

        #OAuth2の資格情報を使用してGoogle APIにログインします。
        gc = gspread.authorize(credentials)

        #共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
        SPREADSHEET_KEY = '1s8Od0cNXnpAX5ongWXN7royzDHNb_nbQSPhD_Ez7KNk'

        #共有設定したスプレッドシートのシート1を開く
        worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
        export_value = title
        worksheet.append_row(export_value)
        return render(
                request,
                "wknapp/index.html",
                context
            )