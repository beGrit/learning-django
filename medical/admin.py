from django.apps import apps
from django.contrib import admin

models = apps.get_models('medical')

for model in models:
    if not admin.site.is_registered(model):
        admin.site.register(model)
