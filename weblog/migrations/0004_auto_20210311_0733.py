# Generated by Django 3.1.6 on 2021-03-11 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weblog', '0003_auto_20210311_0729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='weblog.author'),
        ),
    ]
