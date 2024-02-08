
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from .models import ChatMessage, ChatRoom, User
from channels.db import database_sync_to_async
from django.db.models import Q
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat_'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
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
        
        await self.save_message(room_id, recipient_id, content)
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "sender": sender.username, "message": content}
        )


    async def save_message(self, room_id, recipient_id, content):
        room = await sync_to_async(ChatRoom.objects.get)(id=room_id)
        recipient_id = recipient_id
        sender = self.scope["user"]
        await database_sync_to_async(ChatMessage.objects.create)(room=room, recipient=recipient_id, sender=sender, content=content)
    async def chat_message(self, event):
        message = event["message"]
        sender_username = event["sender"]
        await self.send(text_data=json.dumps({"sender": sender_username, "message": message}))    
    

