# chat/urls.py
from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('advanced/<int:chat_room_id>/', views.room_advanced, name='room-advanced'),
    path('available_chat_rooms/', views.available_chat_channels, name='available-chat-rooms'),
    path('chat_to_user/<int:user_id>', views.chat_to_user, name='chat-to-user'),
    path('chat_to_vaccination_group/<int:group_id>', views.chat_to_vaccination_group, name='chat-to-vaccination-group'),
    path('chat_to_official_account/<int:official_account_id>', views.chat_to_official_account,
         name='chat-to-official-account'),
    path('quit_chat_room/<int:chat_room_id>/', views.quit_chat_room, name='quit-chat-room'),
    path('quit_chat_room_batch/', views.quit_chat_room_batch, name='quit-chat-room-batch'),
]
