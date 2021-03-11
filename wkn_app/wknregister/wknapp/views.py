from django.shortcuts import render, redirect
import json
import sys # ErrorLog出力用
sys.path.append('/Users/startaiyo/opt/anaconda3/lib/python3.8/site-packages')
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView # 追記
from django.contrib.auth.forms import UserCreationForm  # 追記
from django.urls import reverse_lazy

class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "wknapp/create.html"
    success_url = reverse_lazy("login")

@login_required
def home (request):
    context={'equipments':{'パスツールピペット9ディスポーザブル(IK-PAS-9P）': 1936,'Nuncイージーディッシュ\u300035ｍｍ': 11880}}
    return render(request, 'wknapp/home.html', context)
        
def index(request):
    if request.method=="GET":
        return render(
            request,
            "wknapp/index.html",
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
        msg="注文しました。"
        return render(
                request,
                "wknapp/home.html",
                context= { 'msg' :msg }
            )

def user_logout(request):
    logout(request)
    return redirect('user:index')