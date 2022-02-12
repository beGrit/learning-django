from django.contrib import admin

from medical.models import DrugInfo


@admin.register(DrugInfo)
class DrugInfoAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'drug_thumbnail')
    pass
