import json

import redis
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import PasswordInput


class EmailLoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    email = forms.CharField(max_length=100, required=True)
    code = forms.CharField(max_length=10)

    def clean(self):
        # Set code message to redis.
        redis_client = redis.Redis()
        data = redis_client.get(self.cleaned_data.get('email'))
        if data is None:
            self.add_error('code', 'The code is expired.')
        else:
            right_code = json.loads(data)['code']
            input_code = self.cleaned_data.get('code')
            if right_code != input_code:
                self.add_error('code', 'The code is not correct.')
            else:
                username = self.cleaned_data.get('username')
                email = self.cleaned_data.get('email')
                user_cache = User.objects.filter(username=username).filter(email=email).first()
                if user_cache is None:
                    self.add_error('username', 'User not found.')
                    self.add_error('email', 'User not found.')
        return self.cleaned_data


class PasswordLoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True, widget=PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user_cache = authenticate(None, username=username, password=password)
        if user_cache is None:
            self.add_error('username', 'User not found.')
            self.add_error('password', 'User not found.')
        return self.cleaned_data
