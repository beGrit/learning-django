# Generated by Django 3.1.6 on 2021-03-13 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weblog', '0004_auto_20210311_0733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(upload_to=''),
        ),
    ]
