from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
import medical.views

app_name = 'medical'

urlpatterns = [
    path('', medical.views.home_page, name='home-page'),
    path('custom/activity/vaccination/subscribe', medical.views.activity_vaccination_subscribe,
         name='activity-vaccination-subscribe'),
    path('custom/activity/vaccination/subscribe/form/<int:vaccination_id>', medical.views.subscribe_vaccination_form,
         name='activity-vaccination-subscribe-form'),
    path('custom/activity/vaccination/subscribe/success', medical.views.subscribe_vaccination_success,
         name='activity-vaccination-subscribe-success')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
