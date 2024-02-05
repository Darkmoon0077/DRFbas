
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from .models import ChatMessage, ChatRoom, User
from channels.db import database_sync_to_async
from django.db.models import Q
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
    async def disconnect(self, close_code):
        pass
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except Exception as e:
            print("Error in receive method:", e)
        content = data['content']
        room_id = data['room_id']
        sender = self.scope["user"]
        sender_id = sender.id
        recipient_i = data['recipient']
        recipient_id = await sync_to_async(User.objects.get)(pk=recipient_i)
        
        await self.save_message(room_id, recipient_id, sender_id, content)
        await self.send(text_data=json.dumps({
            'message': content,
            'sender': sender.username,
        }))

    @database_sync_to_async
    def save_message(self, room_id, recipient_id, sender_id, content):
        room = ChatRoom.objects.get(id=room_id)
        recipient_id = recipient_id
        sender_id = self.scope["user"]
        ChatMessage.objects.create(room=room, recipient=recipient_id, sender=sender_id, content=content)

    

