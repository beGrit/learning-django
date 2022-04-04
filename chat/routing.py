from django.urls import re_path, path

from chat import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', consumers.GroupChatConsumer.as_asgi()),
    path('ws/chat/group/<str:room_name>/', consumers.GroupChatConsumer.as_asgi()),
    path('ws/chat/solo/<str:room_name>/', consumers.SoloChatConsumer.as_asgi()),
]
