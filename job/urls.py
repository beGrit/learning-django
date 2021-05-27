from django.urls import path, include
from job.views import *

app_name = 'job'

urlpatterns = [
    path('test/', test, name='test')
]
