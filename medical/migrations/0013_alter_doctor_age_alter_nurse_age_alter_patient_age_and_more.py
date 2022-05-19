# Generated by Django 4.0.2 on 2022-05-19 16:30

import datetime
from django.db import migrations, models
import medical.extend.fields


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0012_alter_doctor_age_alter_nurse_age_alter_patient_age_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='age',
            field=medical.extend.fields.AgeField(max_length=20, validators=[medical.extend.fields.AgeField.age_validate, medical.extend.fields.AgeField.age_validate]),
        ),
        migrations.AlterField(
            model_name='nurse',
            name='age',
            field=medical.extend.fields.AgeField(max_length=20, validators=[medical.extend.fields.AgeField.age_validate, medical.extend.fields.AgeField.age_validate, medical.extend.fields.AgeField.age_validate]),
        ),
        migrations.AlterField(
            model_name='patient',
            name='age',
            field=medical.extend.fields.AgeField(max_length=20, validators=[medical.extend.fields.AgeField.age_validate, medical.extend.fields.AgeField.age_validate]),
        ),
        migrations.AlterField(
            model_name='patient',
            name='telphone',
            field=medical.extend.fields.TelPhoneField(max_length=104, validators=[medical.extend.fields.TelPhoneField.tel_phone_validate, medical.extend.fields.TelPhoneField.tel_phone_validate]),
        ),
        migrations.AlterField(
            model_name='staff',
            name='age',
            field=medical.extend.fields.AgeField(max_length=20, validators=[medical.extend.fields.AgeField.age_validate, medical.extend.fields.AgeField.age_validate, medical.extend.fields.AgeField.age_validate, medical.extend.fields.AgeField.age_validate]),
        ),
        migrations.AlterField(
            model_name='vaccinationsubscribe',
            name='telephone',
            field=medical.extend.fields.TelPhoneField(help_text='请输入 XX-XXXXXXXXXXX', max_length=200, null=True, validators=[medical.extend.fields.TelPhoneField.tel_phone_validate, medical.extend.fields.TelPhoneField.tel_phone_validate], verbose_name='手机号码'),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='last_visit_site_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 20, 0, 30, 6, 929147), null=True),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='age',
            field=medical.extend.fields.AgeField(max_length=20, validators=[medical.extend.fields.AgeField.age_validate, medical.extend.fields.AgeField.age_validate, medical.extend.fields.AgeField.age_validate, medical.extend.fields.AgeField.age_validate, medical.extend.fields.AgeField.age_validate]),
        ),
    ]
