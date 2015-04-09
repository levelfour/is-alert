# coding: utf-8
from django.shortcuts import render
from homework_alert.models import User, Homework


def index(request):
    works = Homework.objects.all()
    return render(request, 'homework_alert/index.html', {'works': works})

def login(request):
    error = None
    if request.method == 'POST':
        if request.POST['mail'] == '':
            error = 'メールアドレスを入力してください'
        elif request.POST['password'] == '':
            error = 'パスワードを入力してください'
        else:
            try:
                user = User.objects.get(email=request.POST['mail'])
                if user.check_password(request.POST['password']):
                    return render(request, 'homework_alert/login.html', {'error': 'ログイン成功です'})
                else:
                    error = 'パスワードが違います'
            except User.DoesNotExist as e:
                error = '登録されていないメールアドレスです'
    return render(request, 'homework_alert/login.html', {'error': error})

def signup(request):
    error = None
    if request.method == 'POST':
        if request.POST['mail'] == '':
            error = 'メールアドレスを入力してください'
        elif request.POST['password'] == '' or request.POST['password2'] == '':
            error = 'パスワードを入力してください'
        elif request.POST['password'] != request.POST['password2']:
            error = 'パスワードに誤りがあります'
        else:
            user = User.objects.create(email=request.POST['mail'], password=User.hash_password(request.POST['password']))
            return render(request, 'homework_alert/signup_complete.html', {})
    return render(request, 'homework_alert/signup.html', {'error': error})
