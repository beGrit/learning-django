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
         name='activity-vaccination-subscribe-success'),
    path('custom/epidemic/index', medical.views.epidemic,
         name='epidemic-index'),
    path('custom/hospital/index', medical.views.hospital_list,
         name='hospital-index'),
    path('custom/hospital/details/<int:hospital_id>', medical.views.hospital_details,
         name='hospital-details'),
    path('custom/volunteer/register/form', medical.views.volunteer_register_form,
         name='volunteer-register-form'),
    path('custom/news/list', medical.views.news_list,
         name='news-list'),
    path('custom/news/<slug:pk>/', medical.views.NewsDetailsView.as_view(),
         name='news-detail'),
    path('custom/property', medical.views.property_list,
         name='property-list'),
    path('custom/drugs', medical.views.DrugListView.as_view(),
         name='drug-list'),
    path('custom/equipments', medical.views.EquipmentListView.as_view(),
         name='equipment-list'),
    path('custom/hospitals', medical.views.HospitalListView.as_view(),
         name='hospital-list'),
    path('custom/hospital/<slug:pk>/', medical.views.HospitalDetailView.as_view(),
         name='hospital-detail'),
    path('custom/vaccines', medical.views.VaccineListView.as_view(),
         name='vaccine-list'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
