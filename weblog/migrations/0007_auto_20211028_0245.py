# Generated by Django 3.1.6 on 2021-10-28 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weblog', '0006_auto_20210313_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(upload_to='weblog/static/images/avatars'),
        ),
    ]
