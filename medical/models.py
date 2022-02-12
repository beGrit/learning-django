import datetime

from django.db import models

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
    related_hospital = models.OneToOneField(blank=False, to=Region, on_delete=models.CASCADE)


class OfficeArea(models.Model):
    code_number = models.CharField(blank=False, unique=True, help_text='The office builder code number', max_length=200)
    related_hospital = models.ForeignKey(blank=False, to=Hospital, on_delete=models.CASCADE)


class BuildrArea(models.Model):
    code_number = models.CharField(blank=False, unique=True, help_text='The office builder code number', max_length=200)
    related_office_area = models.ForeignKey(blank=False, to=Hospital, on_delete=models.CASCADE)


'''
Activity
'''


class OrdinaryActivity(models.Model):
    class Meta:
        abstract = True


class COVIDActivity(models.Model):
    class Meta:
        abstract = True


class NucleicAcidTesting(COVIDActivity):
    pass


class Vaccination(COVIDActivity):
    pass
