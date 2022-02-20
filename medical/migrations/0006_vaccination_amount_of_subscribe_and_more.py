# Generated by Django 4.0.2 on 2022-02-13 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0005_alter_buildarea_related_office_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='vaccination',
            name='amount_of_subscribe',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vaccination',
            name='amount_of_vaccine',
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
    ]