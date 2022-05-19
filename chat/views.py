import datetime
import json

from django.contrib.auth.models import User
from django.db import transaction
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from chat.models import ChatRoom, VaccinationChatRoom, OfficialAccount, OfficialChatRoom
from medical.models import Doctor, Vaccination


def room_advanced(request, chat_room_id=None):
    room = ChatRoom.objects.get(id=chat_room_id)
    room_type = ''
    if room is not None:
        if room.type == 1:
            room_type = 'official_account'
        elif room.type == 2:
            room_type = 'group'
        elif room.type == 3:
            room_type = 'solo'
    return render(request, 'chat/components/message/room/room-advanced.html', {
        'room_name': chat_room_id,
        'chat_room_id': chat_room_id,
        'user_id': request.user.id,
        'room_type': room_type,
    })


def available_chat_channels(request):
    doctors = list(Doctor.objects.all())
    vaccinations = list(Vaccination.objects.all())
    official_accounts = list(OfficialAccount.objects.all())
    return render(request, 'chat/components/message/channel/channels.html', {
        'doctors': doctors,
        'vaccinations': vaccinations,
        'official_accounts': official_accounts,
    })


@transaction.atomic
def chat_to_user(request, user_id):
    if request.user.id != user_id:
        user = User.objects.get(id=user_id)
        room = ChatRoom.objects.filter(subscribers__in=[user, request.user]).filter(type=3).first()
        if room is None:
            chat_room = ChatRoom(title=user.username, type=3, open_date_time=datetime.datetime.now())
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
        vaccination_chat_room.save()
    else:
        vaccination = Vaccination.objects.get(id=group_id)
        vaccination_chat_room = VaccinationChatRoom(title=vaccination.title, related_activity=vaccination, type=2,
                                                    open_date_time=datetime.datetime.now())
        vaccination_chat_room.save()
        vaccination_chat_room.subscribers.set([request.user])
        vaccination_chat_room.save()
    return room_advanced(request, chat_room_id=vaccination_chat_room.id)


@transaction.atomic
def chat_to_official_account(request, official_account_id):
    official_account = OfficialAccount.objects.get(id=official_account_id)
    room = OfficialChatRoom.objects.filter(related_official_account=official_account).filter(subscribers__in=[request.user]).first()
    if room is not None:
        return room_advanced(request, chat_room_id=room.id)
    else:
        official_account = OfficialAccount.objects.get(id=official_account_id)
        if official_account is None:
            raise Exception
        else:
            room = OfficialChatRoom(title=official_account.name, related_official_account=official_account,
                                    open_date_time=datetime.datetime.now(), type=1)
            room.save()
            room.subscribers.set([request.user, official_account.related_user])
            room.save()
            return room_advanced(request, chat_room_id=room.id)


@csrf_exempt
def quit_chat_room(request, chat_room_id):
    if chat_room_id is None:
        raise Http404
    else:
        chat_room = ChatRoom.objects.get(id=chat_room_id)
        if request.user not in chat_room.subscribers:
            raise Http404
        else:
            if chat_room.type == 1 or chat_room.type == 3:
                chat_room.delete()
            else:
                chat_room.subscribers.remove(request.user)


@csrf_exempt
@transaction.atomic
def quit_chat_room_batch(request):
    json_response = JsonResponse(data={})
    data = json.loads(request.body)
    id_arr = data['chat_room_id_arr'][0]
    id_arr = list(map(lambda item: int(item), id_arr))
    chat_rooms = list(ChatRoom.objects.filter(id__in=id_arr).all())
    for chat_room in chat_rooms:
        if request.user not in list(chat_room.subscribers.all()):
            raise Exception
        else:
            if chat_room.type == 1 or chat_room.type == 3:
                chat_room.delete()
            else:
                chat_room.subscribers.remove(request.user)
            json_response.content = {
                'message': 'Success deleted.'
            }


def remove_chat_room(request):
    pass
