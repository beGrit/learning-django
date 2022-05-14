import jieba
from django.contrib.auth.models import User
from django.db import models

from medical.models import Vaccination


class AutoReply(models.Model):
    word = models.TextField(max_length=200)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.word


class OfficialAccount(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    profile_picture = models.ImageField(blank=True)
    related_user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    auto_replay_configs = models.ManyToManyField(AutoReply, blank=True)

    def auto_reply(self, content: str):
        seg_list = jieba.cut(content)
        seg_arr = list(seg_list)
        for seg in seg_arr:
            auto_replay_entity = self.auto_replay_configs.filter(word=seg).first()
            if auto_replay_entity is not None:
                return auto_replay_entity.content
        return None


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


class VaccinationChatRoom(ChatRoom):
    related_activity = models.OneToOneField(to=Vaccination, on_delete=models.CASCADE)


class ChatContentCollection(models.Model):
    related_chat_room = models.ForeignKey(ChatRoom, models.CASCADE)

    def __str__(self):
        return self.related_chat_room.title + " 's " + 'ChatContentCollection'


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
