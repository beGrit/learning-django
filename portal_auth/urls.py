from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'portal_auth'

urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name="portal_auth/login_form.html"), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
]
