import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

'''
Property domain.
'''


class Drug(models.Model):
    code = models.CharField(blank=False, help_text='The unique code for drug.', null=True, unique=True, max_length=100)
    name = models.CharField(blank=False, help_text='The drug name.', null=True, max_length=100)
    description = models.TextField(blank=True, help_text='The drug info description.', null=False)
    price = models.FloatField(blank=True, help_text='The drug price.')
    drug_thumbnail = models.ImageField(blank=True, upload_to='medical/images/drug/thumbnail')
    produced_date_time = models.DateTimeField(help_text='The drug produced date time.')
    onboard_date_time = models.DateTimeField(help_text='The drug onboard date time.')
    sales_volume = models.FloatField(help_text='The drug sales volume.')

    class Meta:
        ordering = ['onboard_date_time']
        verbose_name = 'drug'
        verbose_name_plural = 'drugs'


class Equipment(models.Model):
    code = models.CharField(blank=False, help_text='The equipment trade mark.', null=True, unique=True, max_length=100)
    name = models.CharField(blank=False, help_text='Equipment name.', null=True, max_length=100)


'''
User domain.
'''


class CommonPeople(models.Model):
    GenderChoice = [
        (1, 'male'),
        (0, 'female')
    ]
    name = models.CharField(blank=False, null=True, max_length=100)
    gender = models.CharField(blank=False, null=True, choices=GenderChoice, max_length=2)
    age = models.IntegerField(blank=True)
    id_card = models.CharField(blank=False, null=True, max_length=18)
    profile_picture = models.ImageField(blank=True, upload_to='medical/images/common_people/profile')

    class Meta:
        abstract = True


class Civilian(CommonPeople):
    class Meta:
        abstract = True


class Worker(CommonPeople):
    serial_number = models.CharField(blank=False, null=True, max_length=100)
    hire_date_time = models.DateTimeField()
    working_year = models.FloatField(blank=False)

    class Meta:
        abstract = True


class Visitor(Civilian):
    pass


class Patient(Civilian):
    pass


class Doctor(Worker):
    pass


class Nurse(Worker):
    pass


'''
Region domain
'''


class Region(models.Model):
    longitude = models.FloatField(blank=False, help_text='The longitude for hospital.')
    latitude = models.FloatField(blank=False, help_text='The latitude for hospital location.')


class Hospital(models.Model):
    code = models.CharField(blank=False, unique=True, help_text='The code for hospital', max_length=200)
    name = models.CharField(blank=False, help_text='The name for hospital.', max_length=200)
    related_region = models.OneToOneField(blank=False, to=Region, on_delete=models.CASCADE)


class OfficeArea(models.Model):
    code_number = models.CharField(blank=False, unique=True, help_text='The office builder code number', max_length=200)
    name = models.CharField(blank=False, max_length=200)
    related_hospital = models.ForeignKey(blank=False, to=Hospital, on_delete=models.CASCADE)


class BuildArea(models.Model):
    code_number = models.CharField(blank=False, unique=True, help_text='The office builder code number', max_length=200)
    name = models.CharField(blank=False, max_length=200)
    related_office_area = models.ForeignKey(blank=False, to=OfficeArea, on_delete=models.CASCADE)


'''
Activity resources
'''


class Vaccine(models.Model):
    name = models.CharField(blank=False, null=True, max_length=200)
    pass


'''
Activity
'''


class OrdinaryActivity(models.Model):
    class Meta:
        abstract = True


class COVIDActivity(models.Model):
    title = models.CharField(blank=False, null=True, max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        abstract = True


class NucleicAcidTesting(COVIDActivity):
    pass


class Vaccination(COVIDActivity):
    process_date_time = models.DateTimeField()
    publish_date_time = models.DateTimeField()
    related_builder_area = models.ForeignKey(blank=False, to=BuildArea, on_delete=models.CASCADE)
    related_vaccine = models.ForeignKey(blank=False, to=Vaccine, on_delete=models.CASCADE)
    amount_of_subscribe = models.IntegerField(blank=False)
    amount_of_vaccine = models.IntegerField(blank=True)

    @property
    def is_due(self) -> bool:
        if timezone.now() > self.process_date_time:
            return True
        else:
            return False

    @property
    def full_area(self) -> str:
        return self.related_builder_area.related_office_area.related_hospital.name + self.related_builder_area.name + self.related_builder_area.related_office_area.name


class Subscribe(models.Model):
    subscribe_date_time = models.DateTimeField(blank=True, auto_now_add=True)

    class Meta:
        abstract = True


class VaccinationSubscribe(Subscribe):
    name = models.CharField(blank=False, null=True, max_length=200)
    telephone = models.CharField(blank=False, null=True, max_length=200)
    email_address = models.EmailField(blank=True)
    related_vaccination = models.ForeignKey(to=Vaccination, on_delete=models.DO_NOTHING)

    def clean(self):
        Subscribe.clean(self)
        if not self.can_subscribe():
            raise ValidationError('This vaccination can not be subscribe.')

    def can_subscribe(self):
        flag = True
        if self.related_vaccination.is_due:
            flag = False
        if self.related_vaccination.amount_of_subscribe + 1 > self.related_vaccination.amount_of_vaccine:
            flag = False
        return flag
