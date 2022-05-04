# Generated by Django 4.0.2 on 2022-04-23 09:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatContentCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, max_length=200)),
                ('publish_date_time', models.DateTimeField()),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('related_chat_content_collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chatcontentcollection')),
            ],
        ),
        migrations.CreateModel(
            name='MarkedWords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, max_length=200)),
                ('publish_date_time', models.DateTimeField()),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('related_chat_content_collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chatcontentcollection')),
            ],
        ),
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=200)),
                ('type', models.IntegerField(choices=[(1, '公众号聊天'), (2, '群组聊天'), (3, '个人聊天')])),
                ('subscribers', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='chatcontentcollection',
            name='related_chat_room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chatroom'),
        ),
    ]