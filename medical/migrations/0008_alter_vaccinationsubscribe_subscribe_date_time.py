# Generated by Django 4.0.2 on 2022-02-20 05:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0007_vaccinationsubscribe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccinationsubscribe',
            name='subscribe_date_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 20, 5, 38, 38, 263188, tzinfo=utc)),
        ),
    ]
