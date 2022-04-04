from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.ModelForm):
    template_name = 'admin/.html'

    class Meta:
        model = User
        fields = ['username', 'password']
