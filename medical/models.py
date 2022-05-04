import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from medical.extend import fields as extend_model_fields

'''
Property domain.
'''


class Drug(models.Model):
    code = models.CharField(null=True, unique=True, max_length=100)
    name = models.CharField(null=True, max_length=100)
    description = models.TextField(blank=True, help_text='The drug info description.', null=False)
    price = models.FloatField(blank=True, help_text='The drug price.')
    drug_thumbnail = models.ImageField(blank=True, upload_to='medical/images/drug/thumbnail')
    produced_date_time = models.DateTimeField(help_text='The drug produced date time.')
    onboard_date_time = models.DateTimeField(help_text='The drug onboard date time.')
    sales_volume = models.FloatField(blank=True, help_text='销售量')
    storage_volume = models.FloatField(blank=True, help_text='存储量')


class Equipment(models.Model):
    code = models.CharField(blank=False, null=True, unique=True, max_length=100)
    name = models.CharField(blank=False, null=True, max_length=100)
    description = models.TextField(blank=True, null=False)
    price = models.FloatField(blank=True)
    drug_thumbnail = models.ImageField(blank=True, upload_to='medical/images/equipment/thumbnail')
    produced_date_time = models.DateTimeField()
    onboard_date_time = models.DateTimeField()
    sales_volume = models.FloatField(blank=True, help_text='销售量')
    storage_volume = models.FloatField(blank=True, help_text='存储量')


'''
Region domain
'''


class Region(models.Model):
    longitude = models.FloatField(blank=False, help_text='The longitude for hospital.')
    latitude = models.FloatField(blank=False, help_text='The latitude for hospital location.')


class Hospital(models.Model):
    code = models.CharField(blank=False, unique=True, help_text='The code for hospital.', max_length=200)
    name = models.CharField(blank=False, help_text='The name for hospital.', max_length=200)
    description = models.TextField(blank=True, help_text='The description for hospital.')
    related_region = models.OneToOneField(blank=False, to=Region, on_delete=models.CASCADE)


class BuildArea(models.Model):
    code_number = models.CharField(blank=False, unique=True, help_text='The office builder code number', max_length=200)
    name = models.CharField(blank=False, max_length=200)
    related_hospital = models.ForeignKey(blank=False, to=Hospital, on_delete=models.CASCADE)


'''
Activity resources
'''


class Vaccine(models.Model):
    name = models.CharField(blank=False, null=True, max_length=200)
    pass


class DailyIncreaseVirusData(models.Model):
    definite = models.PositiveIntegerField(verbose_name='确诊')
    cure = models.PositiveIntegerField(verbose_name='本土')
    dead = models.PositiveIntegerField(verbose_name='境外输入')
    asymptomatic = models.PositiveIntegerField(verbose_name='无症状')
    date = models.DateField()


class StaticsVirusData(models.Model):
    definite = models.PositiveIntegerField(verbose_name='确诊')
    cure = models.PositiveIntegerField(verbose_name='治愈')
    dead = models.PositiveIntegerField(verbose_name='死亡')


'''
Activity
'''


class Activity(models.Model):
    class Meta:
        abstract = True


class OrdinaryActivity(Activity):
    pass


class COVIDActivity(Activity):
    title = models.CharField(blank=False, null=True, max_length=200)
    description = models.TextField(blank=True)
    process_date_time = models.DateTimeField()
    publish_date_time = models.DateTimeField()


class Vaccination(COVIDActivity):
    related_builder_area = models.ForeignKey(to=BuildArea, on_delete=models.CASCADE)
    related_vaccine = models.ForeignKey(null=True, to=Vaccine, on_delete=models.SET_NULL)
    amount_of_subscribe = models.PositiveIntegerField()
    amount_of_vaccine = models.PositiveIntegerField()

    @property
    def is_due(self) -> bool:
        if timezone.now() > self.process_date_time:
            return True
        else:
            return False

    @property
    def full_area(self) -> str:
        return self.related_builder_area.related_hospital.name + self.related_builder_area.name


class Subscribe(models.Model):
    subscribe_date_time = models.DateTimeField(blank=True, auto_now_add=True)

    class Meta:
        abstract = True


class VaccinationSubscribe(Subscribe):
    name = models.CharField(null=True, max_length=200, verbose_name='姓名')
    telephone = models.CharField(null=True, max_length=200, verbose_name='手机号码',
                                 help_text='请输入 +08-XXXXXXXXXXX')
    email_address = models.EmailField(verbose_name='邮箱地址')
    address = models.CharField(blank=True, max_length=200, verbose_name='家庭住址')
    birth = models.DateField(verbose_name='出生日期')
    person_photo = models.FileField(blank=True, verbose_name='个人照片')
    related_vaccination = models.ForeignKey(to=Vaccination, on_delete=models.DO_NOTHING)

    def clean(self):
        Subscribe.clean(self)
        if not self.can_subscribe():
            raise ValidationError('This vaccination can not be subscribe.')

    def can_subscribe(self) -> bool:
        flag = True
        # The vaccination is due.
        if self.related_vaccination.is_due:
            flag = False
        # Check the number of the available vaccine.
        if self.related_vaccination.amount_of_subscribe + 1 > self.related_vaccination.amount_of_vaccine:
            flag = False
        return flag


'''
User domain.
'''


class Medicalor(models.Model):
    name = models.CharField(blank=False, null=True, max_length=100)
    gender = extend_model_fields.GenderField(blank=False, null=True)
    age = extend_model_fields.AgeField(blank=False)
    work_year = models.PositiveIntegerField(help_text='The years of working.')
    hire_date = models.DateField(null=True, default=datetime.datetime.now)
    salary = models.PositiveIntegerField(blank=False, default=0)
    profile_picture = models.ImageField(blank=True, upload_to='medical/images/common_people/profile',
                                        default='medical/images/project/avatar01.jpeg')
    related_user = models.ForeignKey(to=User, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class Doctor(Medicalor):
    education_background = extend_model_fields.EducationBackgroundField(blank=False)
    doctor_qualification = models.IntegerField(blank=False, choices=[
        (1, '住院医师（助教）'),
        (2, '主治医师（讲师）'),
        (3, '副主任医师（副教授）'),
        (4, '主任医师（教授）')
    ])
    related_area = models.ForeignKey(blank=True, to=BuildArea, null=True, on_delete=models.SET_NULL)

    def do_mail(self):
        pass


class Nurse(Medicalor):
    education_background = extend_model_fields.EducationBackgroundField(blank=False)
    nurse_qualification = models.IntegerField(blank=False, choices=[
        (1, '初级护士'),
        (2, '中级护士'),
        (3, '高级护士'),
    ])


class Supportor(Medicalor):
    support_type = models.IntegerField(blank=False, choices=[
        (1, '临时工'),
        (2, '外派人员'),
        (3, '正式员工'),
    ])

    class Meta:
        abstract = True


class Staff(Supportor):
    due_description = models.TextField(blank=True, max_length=200, help_text="职责描述")


class Volunteer(Supportor):
    work_date = models.DateTimeField(blank=False, verbose_name='工作日期', help_text='选择你要工作的日期时间')
    is_student = models.IntegerField(blank=False, default=0, choices=[
        (0, '不是'),
        (1, '是')
    ], verbose_name='是否是学生')
    no_salary = models.IntegerField(blank=False, default=0, choices=[
        (0, '无'),
        (1, '有')
    ], verbose_name='是否需要工资')
    related_activity = models.ForeignKey(blank=False, to=COVIDActivity, on_delete=models.SET_NULL, null=True,
                                         verbose_name='报名参加的活动')


class CommonPeople(models.Model):
    name = models.CharField(blank=False, null=True, max_length=100)
    gender = extend_model_fields.GenderField(blank=False, null=True)
    age = extend_model_fields.AgeField(blank=False)
    email = models.EmailField(blank=False)
    telphone = extend_model_fields.TelPhoneField(blank=False)
    profile_picture = models.ImageField(blank=True, upload_to='medical/images/common_people/profile',
                                        default='medical/images/project/avatar01.jpeg')

    class Meta:
        abstract = True


class Visitor(CommonPeople):
    last_visit_site_time = models.DateTimeField(blank=False, null=True, default=datetime.datetime.now())
    visit_times = models.PositiveIntegerField(blank=False, null=True, default=0)


class Patient(CommonPeople):
    related_department = models.ForeignKey(blank=False, null=True, to=BuildArea, on_delete=models.CASCADE)
    related_doctor = models.ForeignKey(blank=False, null=True, to=Doctor, on_delete=models.SET_NULL)


'''NEWS'''


class News(models.Model):
    image_url_path = models.FileField(blank=True)
    title = models.TextField(max_length=200)
    content = models.TextField(blank=True, max_length=200)
    author = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    publish_date_time = models.DateTimeField()
