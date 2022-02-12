from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

import medical.views

app_name = 'medical'

urlpatterns = [
    path('', medical.views.home_page, name='home-page'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)