from django.contrib.auth.models import User
from django.db import models

from medical.models import Vaccination


class OfficialAccount(models.Model):
    pass


class ChatRoom(models.Model):
    title = models.TextField(max_length=200)
    type = models.IntegerField(choices=[
        (1, '公众号聊天'),
        (2, '群组聊天'),
        (3, '个人聊天'),
    ])
    subscribers = models.ManyToManyField(User)
    open_date_time = models.DateTimeField()


class GroupChatRoom(ChatRoom):
    pass


class OfficialChatRoom(ChatRoom):
    related_official_account = models.OneToOneField(to=OfficialAccount, on_delete=models.CASCADE)

    def clean_fields(self, exclude=None):
        if self.subscribers.count() != 1:
            raise Exception


class VaccinationChatRoom(ChatRoom):
    related_activity = models.OneToOneField(to=Vaccination, on_delete=models.CASCADE)


class ChatContentCollection(models.Model):
    related_chat_room = models.ForeignKey(ChatRoom, models.CASCADE)


class Message(models.Model):
    content = models.TextField(blank=True, max_length=200)
    related_chat_content_collection = models.ForeignKey(ChatContentCollection, models.CASCADE)
    publisher = models.ForeignKey(User, models.CASCADE)
    publish_date_time = models.DateTimeField()


class MarkedWords(models.Model):
    content = models.TextField(blank=True, max_length=200)
    related_chat_content_collection = models.ForeignKey(ChatContentCollection, models.CASCADE)
    publisher = models.ForeignKey(User, models.CASCADE)
    publish_date_time = models.DateTimeField()
