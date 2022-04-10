import datetime
import json

import redis
from django.core import mail
from django.http import JsonResponse
from django.shortcuts import render
from django.template import Template, loader

from portal_auth.forms import EmailLoginForm


def login_email(request):
    if request.method == 'GET':
        code_flag = request.GET.get('code_flag', False)
        return render(request, 'portal_auth/login_email_form.html', {
            'form': EmailLoginForm(),
            'code_flag': code_flag,
        })
    elif request.method == 'POST':
        pass


def send_code(request, email: str = None):
    if email is None:
        return JsonResponse(code=400, data=None)
    # Build the login code message.
    code = '5555'
    expire_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
    login_code_message = {
        'key': email,
        'code': code,
        'expire_time': str(expire_time),
    }
    # Set code message to redis.
    redis_client = redis.Redis()
    redis_client.set(login_code_message['key'], json.dumps(login_code_message))
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
    return JsonResponse(data=login_code_message)
