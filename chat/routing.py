from django.urls import re_path, path

from chat import consumers

websocket_urlpatterns = [
    path('ws/chat/<int:chat_room_id>/', consumers.GroupChatConsumer.as_asgi()),
    path('ws/chat/group/<int:chat_room_id>/', consumers.GroupChatConsumer.as_asgi()),
    path('ws/chat/solo/<int:chat_room_id>/', consumers.SoloChatConsumer.as_asgi()),
    path('ws/chat/official_account/<int:chat_room_id>/', consumers.OfficialChatConsumer.as_asgi()),
]
