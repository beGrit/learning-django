from django.contrib import admin

from medical.models import Drug, Doctor


@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'drug_thumbnail')
    pass


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    pass
