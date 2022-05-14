from django import template
from django.contrib.auth.models import User
from django.db.models.functions import Lower

from chat.models import ChatRoom, ChatContentCollection

register = template.Library()


@register.inclusion_tag('chat/components/message/message/message_list.html')
def message_detail(user_id, chat_room_id):
    user = User.objects.get(id=user_id)
    chat_room = ChatRoom.objects.filter(subscribers__in=[user]).filter(id=chat_room_id).first()
    chat_collection: ChatContentCollection = chat_room.chatcontentcollection_set.first()
    messages = []
    data = []
    if chat_collection is not None:
        messages = chat_collection.message_set.all()
    for message in messages:
        if message.publisher_id == user_id:
            message_type = 'outgoing'
        else:
            message_type = 'incoming'
        data.append({
            'user': {
                'avatar_path': '/avatar01.jpeg',
                'name': message.publisher.username,
            },
            'datetime': message.publish_date_time,
            'msg_data': {
                'data': message.content
            },
            'type': message_type,
        })
    return {
        'data_list': data,
    }


@register.inclusion_tag('chat/components/message/message_queue/card_list.html')
def message_queue(user_id, active_room_id=None):
    user = User.objects.filter(id=user_id).first()
    chat_rooms = list(user.chatroom_set.all())
    data = []
    for chat_room in chat_rooms:
        if chat_room.type == 3:
            to_user = chat_room.subscribers.exclude(id=user_id).first()
        else:
            to_user = chat_room.subscribers.first()
        message_collection = chat_room.chatcontentcollection_set.first()
        if message_collection is not None:
            message_entity = message_collection.message_set.order_by('-publish_date_time').first()
            first_message = message_entity.content
            last_send_time = message_entity.publish_date_time
        else:
            first_message = ''
            last_send_time = chat_room.open_date_time
        data.append(
            {
                'chat_room_id': chat_room.id,
                'chat_room': chat_room.title,
                'meta_info': {
                    'type': chat_room.get_type_display(),
                    'last_send_time': last_send_time,
                },
                'user_info':
                    {
                        'avatar_path': '/avatar01.jpeg',
                        'name': to_user.username,
                    },
                'message': first_message,
            },
        )
    data.sort(key=lambda x: (x['meta_info']['last_send_time']), reverse=True)
    return {
        'data': data,
    }
