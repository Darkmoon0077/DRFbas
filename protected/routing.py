from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from authorz.consumers import ChatConsumer
from django.core.asgi import get_asgi_application
websocket_urlpatterns = [
    path("ws/chat/<room_id>/", ChatConsumer.as_asgi()),
]