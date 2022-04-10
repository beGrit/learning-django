import datetime

from django import template

register = template.Library()


@register.inclusion_tag('chat/components/message/card_list.html')
def message_queue(chat_room=None):
    data = [
        {
            'chat_room': 'room-1',
            'meta_info': {
                'type': 'solo',
                'last_send_time': datetime.datetime.now(),
            },
            'user_info':
                {
                    'avatar_path': '/chat/images/img.png',
                    'name': 'pocky',
                },
            'message': 'Test, which is a new approach to have',
        },
        {
            'chat_room': 'room-2',
            'meta_info': {
                'type': 'solo',
                'last_send_time': datetime.datetime.now(),
            },
            'user_info':
                {
                    'avatar_path': '/chat/images/img.png',
                    'name': 'pocky',
                },
            'message': 'Test, which is a new approach to have',
        },
    ]

    if chat_room is not None:
        for data_item in data:
            if data_item['chat_room'] == chat_room:
                setattr(data_item, 'is_active', True)
    else:
        setattr(data[0], 'is_active', True)
    return {
        'data': data,
    }


def message_detail():
    data = [

    ]
    return {

    }
