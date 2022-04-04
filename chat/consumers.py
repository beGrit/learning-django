# chat/consumers.py
import datetime
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User


class ChatConsumerBase(WebsocketConsumer):
    room_type = ''

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.room_name = None

    def connect(self):
        self.room_name = self.room_type + '_' + self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user,
            }
        )


class GroupChatConsumer(ChatConsumerBase):
    room_type = 'group'

    def chat_message(self, event):
        # Receive message from room group
        message = event['message']
        user: User = self.scope['user']
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'user': {
                'avatar_path': '/static/medical/images/hospital/badge/img_01.png',
                'name': user.username,
            },
            'time': now_time,
            'message': message,
        }))


class SoloChatConsumer(ChatConsumerBase):
    room_type = 'solo'

    def chat_message(self, event):
        now_datetime = datetime.datetime.now()
        if self.scope['user'].username == event['user']['user_name']:
            message_type = 'outgoing'
        else:
            message_type = 'incoming'
        # Send message to WebSocket
        self.send(text_data=json.dumps(
            {
                'user': {
                    'avatar_path': '/chat/images/img.png',
                    'name': 'pocky',
                },
                'datetime': {
                    'data': now_datetime.strftime('%I:%M %p | %m 月 %d 日'),
                    'date': now_datetime.strftime('%m 月 %d 日'),
                    'time': now_datetime.strftime('%I:%M'),
                    'flag': now_datetime.strftime('%p'),
                },
                'msg_data': {
                    'data': event['message'],
                },
                'type': message_type,
            },
        ))
