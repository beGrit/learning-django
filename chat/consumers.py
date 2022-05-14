# chat/consumers.py
import datetime
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from django.shortcuts import render

from chat.models import Message, ChatContentCollection, ChatRoom


class ChatConsumerBase(WebsocketConsumer):
    room_type = ''

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.room_name = None

    def connect(self):
        self.room_name = self.room_type + '_' + str(self.scope['url_route']['kwargs']['chat_room_id'])
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
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'data': text_data_json,
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
        # Extract the data from event.
        receiver_user_id = self.scope['user'].id
        publish_date_time = datetime.datetime.now()
        sender_user_id = self.scope['user'].id
        sender_user = User.objects.filter(id=sender_user_id).first()
        message_data = event['data']['message']
        chat_room_id = event['data']['chat_room_id']
        chat_room = ChatRoom.objects.get(id=chat_room_id)
        if receiver_user_id == sender_user_id:
            message_type = 'outgoing'
        else:
            message_type = 'incoming'
        if message_type == 'outgoing':
            # Save message to the db.
            chat_content_collection = ChatContentCollection.objects.filter(related_chat_room_id=chat_room_id).first()
            if chat_content_collection is None:
                chat_content_collection = ChatContentCollection(related_chat_room=chat_room)
                chat_content_collection.save()
            message_entity = Message(content=message_data,
                                     related_chat_content_collection=chat_content_collection,
                                     publisher=sender_user,
                                     publish_date_time=publish_date_time)
            message_entity.save()
        # Send message to WebSocket
        data = {
            'user': {
                'avatar_path': '/avatar01.jpeg',
                'name': sender_user.username,
            },
            'datetime': publish_date_time,
            'msg_data': {
                'data': message_data,
            },
            'type': message_type,
        }
        message_html = render(None, 'chat/components/message/message/message.html', {
            'data': data,
        })
        self.send(bytes_data=message_html.getvalue())
