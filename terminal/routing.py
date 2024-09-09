from django.urls import path
from .consumers import SSHConsumer

websocket_urlpatterns = [
  path('ws/ssh/', SSHConsumer.as_asgi()),
]