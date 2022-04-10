from django import forms


class EmailLoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    email = forms.CharField(max_length=100, required=True)
    code = forms.CharField(max_length=10)
