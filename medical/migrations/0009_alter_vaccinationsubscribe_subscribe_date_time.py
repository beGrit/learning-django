# Generated by Django 4.0.2 on 2022-02-20 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0008_alter_vaccinationsubscribe_subscribe_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccinationsubscribe',
            name='subscribe_date_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
