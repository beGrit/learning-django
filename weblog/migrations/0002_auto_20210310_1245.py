# Generated by Django 3.1.6 on 2021-03-10 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weblog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='authors',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='mod_date',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='entry',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='weblog.author'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='number_of_comments',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='entry',
            name='number_of_pingbacks',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='entry',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
