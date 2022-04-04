import datetime

from django.shortcuts import render


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name,
    })


def room_advanced(request, room_name):
    now_datetime = datetime.datetime.now()
    msg_list = [
        {
            'user': {
                'avatar_path': '/chat/images/img.png',
                'name': 'pocky',
            },
            'datetime': {
                'data': now_datetime,
                'date': now_datetime.strftime('%m 月 %d 日'),
                'time': now_datetime.strftime('%I:%M'),
                'flag': now_datetime.strftime('%p'),
            },
            'msg_data': {
                'data': 'Test, which is a new approach to have'
            },
            'type': 'incoming',
        },
        {
            'user': {
                'avatar_path': '/chat/images/img.png',
                'name': 'pocky',
            },
            'datetime': {
                'data': now_datetime,
                'date': now_datetime.strftime('%m 月 %d 日'),
                'time': now_datetime.strftime('%I:%M'),
                'flag': now_datetime.strftime('%p'),
            },
            'msg_data': {
                'data': 'Test which is a new approach to have all solutions',
            },
            'type': 'outgoing',
        },
        {
            'user': {
                'avatar_path': '/chat/images/img.png',
                'name': 'pocky',
            },
            'datetime': {
                'data': now_datetime,
                'date': now_datetime.strftime('%m 月 %d 日'),
                'time': now_datetime.strftime('%I:%M'),
                'flag': now_datetime.strftime('%p'),
            },
            'msg_data': {
                'data': 'Test which is a new approach to have all solutions',
            },
            'type': 'outgoing',
        },
    ]
    return render(request, 'chat/room-advanced.html', {
        'room_name': room_name,
        'user': {
            'user_name': request.user.username
        },
        'msg_list': msg_list,
    })
