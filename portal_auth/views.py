import datetime
import json
import random

import redis
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core import mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template import Template, loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from portal_auth.forms import EmailLoginForm, PasswordLoginForm


def login_email(request):
    if request.method == 'GET':
        code_flag = request.GET.get('code_flag', False)
        return render(request, 'portal_auth/login_email_form.html', {
            'form': EmailLoginForm(),
            'code_flag': code_flag,
        })
    elif request.method == 'POST':
        pass


@csrf_exempt
def send_code(request):
    if request.method == 'POST':
        email: str = json.loads(request.body)['email']
        if email is None or email == '':
            return JsonResponse(status=400, data={
                'message': 'The email param is not found.',
                'data': []
            })
        # Build the login code message.
        code = random.randint(1000, 9999)
        expire_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
        login_code_message = {
            'key': email,
            'code': code,
            'expire_time': str(expire_time),
            'message': 'Send code success',
        }
        user_list = list(User.objects.filter(email=email))
        if len(user_list) <= 0:
            return JsonResponse(status=400, data={
                'message': 'The email is not register.',
                'data': []
            })
        # Set code message to redis.
        redis_client = redis.Redis()
        if redis_client.get(login_code_message['key']) is not None:
            return JsonResponse(status=400, data={
                'message': 'The key is exists.',
                'data': []
            })
        redis_client.setex(login_code_message['key'], datetime.timedelta(minutes=1), json.dumps(login_code_message))
        # Send code message to user.
        template: Template = loader.get_template('email/portal_auth/login_code.html')
        body_data = template.render(context={
            'data': login_code_message,
        })
        mail.send_mail(
            '登录校验码，请查收！！！',
            '',
            '1134187280@qq.com',
            recipient_list=[
                email
            ],
            html_message=body_data)
        return JsonResponse(status=200, data=login_code_message)


def login_page(request):
    login_type = request.GET.get('type')
    if login_type is None:
        login_type = 'password'
    data = {
        'password': {
            'display_value': 'Password Login',
            'active': False,
        },
        'email': {
            'display_value': 'Email Login',
            'active': False,
        }
    }
    data[login_type]['active'] = True
    if login_type == 'password':
        form = PasswordLoginForm()
    elif login_type == 'email':
        form = EmailLoginForm()
    else:
        form = PasswordLoginForm()
    if request.method == 'GET':
        return render(request, 'portal_auth/login_page.html', context={
            'data': data,
            'form': form,
            'login_type': login_type,
        })
    elif request.method == 'POST':
        if login_type == 'password':
            form = PasswordLoginForm(request.POST)
            form.full_clean()
            if form.is_valid():
                login(request, user=User.objects.filter(username=form.cleaned_data.get('username')).first())
                return redirect(reverse('medical:home-page'))
            else:
                return render(request, 'portal_auth/login_page.html', context={
                    'data': data,
                    'form': form,
                    'login_type': login_type,
                })
        elif login_type == 'email':
            form = EmailLoginForm(request.POST)
            form.full_clean()
            if form.is_valid():
                login(request, user=User.objects.filter(username=form.cleaned_data.get('username')).first())
                return redirect(reverse('medical:home-page'))
            else:
                return render(request, 'portal_auth/login_page.html', context={
                    'data': data,
                    'form': form,
                    'login_type': login_type,
                })


def register(request):
    user = User({

    })
