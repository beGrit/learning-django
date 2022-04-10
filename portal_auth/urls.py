from django.urls import path
from django.contrib.auth import views as auth_views
from portal_auth import views as portal_auth_views

app_name = 'portal_auth'

urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name="portal_auth/login_form.html"), name='login'),
    path('login/email', portal_auth_views.login_email, name='login-email'),
    path('login/email/send_code/<str:email>', portal_auth_views.send_code, name='login-email-send-code'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
]
