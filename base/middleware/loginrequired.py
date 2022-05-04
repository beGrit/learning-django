from django.shortcuts import redirect
from django.urls import reverse

from learning import settings


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_url = settings.LOGIN_URL
        self.open_urls = [reverse(self.login_url)]

    def __call__(self, request):
        if not request.user.is_authenticated and request.path_info not in self.open_urls:
            return redirect(reverse(self.login_url))
        return self.get_response(request)
