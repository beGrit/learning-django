from django.urls import reverse

from learning import settings


class SpecialRoleContent:
    def __init__(self, response):
        self.get_response = response
        self.login_url = settings.LOGIN_URL
        self.open_urls = [reverse(self.login_url)]
