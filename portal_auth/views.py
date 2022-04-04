from django.contrib.admin.forms import AdminAuthenticationForm
from django.shortcuts import render


# Create your views here.


def login(request):
    return render(request, 'portal_auth/login_form.html', {
        'form': AdminAuthenticationForm()
    })
