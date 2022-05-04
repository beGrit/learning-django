# chat/urls.py
from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('advanced/<str:chat_room_id>', views.room_advanced, name='room-advanced'),
    path('available_chat_rooms/', views.available_chat_channels, name='available-chat-rooms'),
    path('chat_to_user/<int:user_id>', views.chat_to_user, name='chat-to-user'),
    path('chat_to_vaccination_group/<int:group_id>', views.chat_to_vaccination_group, name='chat-to-vaccination-group')
]
