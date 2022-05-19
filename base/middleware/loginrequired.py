import datetime

from django.shortcuts import redirect
from django.urls import reverse

from medical.models import Visitor
from portal_auth.urls import urlpatterns as portal_auth_urlpatterns
from portal_auth.urls import app_name as portal_auth_app_name
from learning import settings


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_url = settings.LOGIN_URL
        self.open_urls = []
        for path in portal_auth_urlpatterns:
            self.open_urls.append(reverse(portal_auth_app_name + ':' + path.name))

    def __call__(self, request):
        if not request.user.is_authenticated and request.path_info not in self.open_urls:
            # Save visitor data.
            # Prepare data.
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            last_visit_site_time = datetime.datetime.now()
            visitor = Visitor.objects.filter(ip_address=ip).first()
            if visitor is None:
                visitor = Visitor(ip_address=ip, visit_times=0, last_visit_site_time=last_visit_site_time)
            else:
                visitor.visit_times += 1
                visitor.last_visit_site_time = last_visit_site_time
            visitor.save()
            return redirect(reverse(self.login_url))
        return self.get_response(request)
