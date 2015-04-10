# coding: utf-8
from django.shortcuts import render, redirect
from homework_alert.models import User, Homework


def check_login(request):
    if request.session.get('isal_u', None) != None and request.session.get('isal_t', None) != None:
        user = User.objects.get(user_token=request.session['isal_u'])
        # TODO: if user does not exists
        if user.access_token == request.session['isal_t']:
            user.update_token()
            request.session['isal_t'] = user.access_token
            return True
    else:
        return False

def index(request):
    works = Homework.objects.all()
    login = check_login(request)
    user = None
    if login:
        user = User.objects.get(user_token=request.session['isal_u'])
    return render(request, 'homework_alert/index.html', {'works': works, 'login': login, 'user': user})

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
                    request.session['isal_u'] = user.user_token
                    request.session['isal_t'] = user.access_token
                    return redirect(index)
                else:
                    error = 'パスワードが違います'
            except User.DoesNotExist as e:
                error = '登録されていないメールアドレスです'
    return render(request, 'homework_alert/login.html', {'error': error})

def logout(request):
    if check_login(request):
        del request.session['isal_u']
        del request.session['isal_t']
    return redirect(index)

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
            user = User.objects.create(
                    email=request.POST['mail'],
                    password=User.hash_password(request.POST['password']))
            user.generate_user_token()
            user.update_token()
            return render(request, 'homework_alert/signup_complete.html', {})
    return render(request, 'homework_alert/signup.html', {'error': error})
