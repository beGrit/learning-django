import uuid

from django.apps import apps
from django.contrib import admin, messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from chat.models import ChatRoom, Message, OfficialAccount, AutoReply
from medical.models import Drug, News, Doctor, Hospital, Vaccination, Equipment, Nurse, Patient, Vaccine, Volunteer, \
    Staff, DailyIncreaseVirusData, StaticsVirusData, VaccinationSubscribe


# Medical admin.
class BaseAdmin(admin.ModelAdmin):
    search_help_text = '可检索所有字段'

    list_per_page = 10

    actions = ['export_selected_objects']

    def get_sortable_by(self, request):
        return self.get_list_display(request)

    def get_search_fields(self, request):
        return self.get_list_display(request)

    @admin.action(description='Export selected items.')
    def export_selected_objects(self, request, queryset):
        selected = queryset.values_list('pk', flat=True)
        ct = ContentType.objects.get_for_model(queryset.model)
        return HttpResponseRedirect('/export/?ct=%s&ids=%s' % (
            ct.pk,
            ','.join(str(pk) for pk in selected),
        ))


@admin.register(Drug)
class DrugAdmin(BaseAdmin):
    actions = ['make_unpublished', 'make_published']

    def get_list_display(self, request):
        return ['code', 'name', 'price']

    def get_ordering(self, request):
        return ['produced_date_time']

    @admin.action(description='Un Publish selected drugs')
    def make_unpublished(self, request, queryset):
        update_count = queryset.update(publish_status=0)
        self.message_user(request, [
            '%d drugs was successfully marked as unpublished.' % update_count,
        ], level=messages.SUCCESS)

    @admin.action(description='Publish selected drugs')
    def make_published(self, request, queryset):
        update_count = queryset.update(publish_status=1)
        self.message_user(request, [
            '%d drugs was successfully marked as published.' % update_count,
        ], level=messages.SUCCESS)


@admin.register(Equipment)
class EquipmentAdmin(BaseAdmin):
    def get_list_display(self, request):
        return ['code', 'name', 'price', 'produced_date_time', 'onboard_date_time']

    def get_ordering(self, request):
        return ['produced_date_time']


@admin.register(News)
class NewsAdmin(BaseAdmin):
    def get_list_display(self, request):
        return ['title', 'publish_date_time']


class MedicalorAdmin(BaseAdmin):
    def get_list_display(self, request):
        return ['name', 'gender', 'age', 'work_year', 'hire_date', 'profile_picture']


@admin.register(Doctor)
class DoctorAdmin(MedicalorAdmin):
    def get_list_display(self, request):
        list_display = super(DoctorAdmin, self).get_list_display(request)
        list_display += ['education_background', 'doctor_qualification']
        return list_display


@admin.register(Nurse)
class NurseAdmin(MedicalorAdmin):
    def get_list_display(self, request):
        list_display = super(NurseAdmin, self).get_list_display(request)
        list_display += ['education_background', 'nurse_qualification']
        return list_display


@admin.register(Patient)
class PatientAdmin(BaseAdmin):
    list_display = ['name', 'gender', 'age']


@admin.register(Hospital)
class HospitalAdmin(MedicalorAdmin):
    def get_list_display(self, request):
        return ['code', 'name']


@admin.register(Vaccine)
class VaccineAdmin(BaseAdmin):
    list_display = ['name', 'description']


@admin.register(Volunteer)
class VolunteerAdmin(BaseAdmin):
    list_display = ['name', 'gender', 'age', 'is_student', 'approved_status']

    actions = ['make_selected_approved']

    @admin.action(description='Make selected volunteers approved')
    def make_selected_approved(self, request, queryset):
        update_count = queryset.update(approved_status=2)
        volunteers = queryset.all()
        for volunteer in volunteers:
            volunteer.send_approved_email()
        self.message_user(request, [
            '%d selected volunteers marked as approved.' % update_count,
        ], level=messages.SUCCESS)


@admin.register(Vaccination)
class VaccinationAdmin(BaseAdmin):
    actions = ['create_chat_room']

    def get_list_display(self, request):
        return ['title', 'process_date_time', 'publish_date_time', 'amount_of_subscribe', 'amount_of_vaccine']

    @admin.action(description='Create chat room.')
    def create_chat_room(self, request, queryset):
        pass


@admin.register(VaccinationSubscribe)
class VaccinationSubscribeAdmin(BaseAdmin):
    list_display = ['name', 'telephone', 'email_address', 'birth', ]
    pass


@admin.register(Staff)
class StaffAdmin(BaseAdmin):
    list_display = ['name', 'gender', 'age', 'support_type', ]


@admin.register(DailyIncreaseVirusData)
class DailyIncreaseVirusDataAdmin(BaseAdmin):
    actions = ['collect_selected_data']

    list_display = ['date', 'definite', 'cure', 'dead', 'asymptomatic']

    @admin.action(description='Collected Selected Data, and export as statics data.')
    def collect_selected_data(self, request, queryset):
        entities = list(queryset.all())
        if len(entities) != 0:
            statics_virus_data_entity = StaticsVirusData()
            statics_virus_data_entity.type = 1
            statics_virus_data_entity.label = str(uuid.uuid4())
            statics_virus_data_entity.definite = 0
            statics_virus_data_entity.cure = 0
            statics_virus_data_entity.dead = 0
            statics_virus_data_entity.asymptomatic = 0
            for entity in entities:
                statics_virus_data_entity.definite += entity.definite
                statics_virus_data_entity.cure += entity.cure
                statics_virus_data_entity.dead += entity.dead
                statics_virus_data_entity.asymptomatic += entity.asymptomatic
            statics_virus_data_entity.save()
            self.message_user(request, [
                '%d virus data was successfully collect, please check in the StaticsVirusData.' % len(entities),
            ], level=messages.SUCCESS)
        else:
            self.message_user(request, [
                'There was not selected any entities.',
            ], level=messages.ERROR)


@admin.register(StaticsVirusData)
class StaticsVirusDataAdmin(BaseAdmin):
    list_display = ['label', 'type', 'definite', 'cure', 'dead', 'asymptomatic']


# Chat admin.
@admin.register(ChatRoom)
class ChatRoomAdmin(BaseAdmin):
    def get_list_display(self, request):
        return ['title', 'type', 'open_date_time']


@admin.register(Message)
class MessageAdmin(BaseAdmin):
    list_display = ['publisher', 'publish_date_time']


@admin.register(OfficialAccount)
class OfficialAccountAdmin(BaseAdmin):
    list_display = ['name', 'description']


@admin.register(AutoReply)
class AutoReplyAdmin(BaseAdmin):
    list_display = ['word', 'content']


models = apps.get_models()

for model in models:
    if not admin.site.is_registered(model):
        admin.site.register(model)
