import datetime

from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render

from chat.models import ChatRoom, VaccinationChatRoom
from medical.models import Doctor, Vaccination


def index(request):
    return render(request, 'chat/index.html')


def room_advanced(request, chat_room_id):
    return render(request, 'chat/components/message/room/room-advanced.html', {
        'room_name': chat_room_id,
        'chat_room_id': chat_room_id,
        'user_id': request.user.id,
    })


def available_chat_channels(request):
    doctors = list(Doctor.objects.all())
    vaccinations = list(Vaccination.objects.all())
    return render(request, 'chat/components/message/channel/channels.html', {
        'doctors': doctors,
        'vaccinations': vaccinations,
    })


@transaction.atomic
def chat_to_user(request, user_id):
    if request.user.id != user_id:
        user = User.objects.get(id=user_id)
        room = ChatRoom.objects.filter(subscribers__in=[user, request.user]).first()
        if room is None:
            chat_room = ChatRoom(title=user.username, type=3)
            chat_room.save()
            chat_room.subscribers.set([user, request.user])
            chat_room.save()
            return room_advanced(request, chat_room_id=chat_room.id)
        else:
            return room_advanced(request, chat_room_id=room.id)
    return available_chat_channels(request)


@transaction.atomic
def chat_to_vaccination_group(request, group_id):
    vaccination_chat_room = VaccinationChatRoom.objects.filter(related_activity_id=group_id).first()
    if vaccination_chat_room is not None:
        vaccination_chat_room.subscribers.add(request.user)
    else:
        vaccination = Vaccination.objects.get(id=group_id)
        vaccination_chat_room = VaccinationChatRoom(title=vaccination.title, related_activity=vaccination, type=2,
                                                    open_date_time=datetime.datetime.now())
        vaccination_chat_room.save()
        vaccination_chat_room.subscribers.set([request.user])
        vaccination_chat_room.save()
    return room_advanced(request, chat_room_id=vaccination_chat_room.id)
