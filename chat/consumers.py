import json
from django.utils import timezone
from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
from channels.consumer import SyncConsumer
from auth_and_reg.models import CustomUser
from chat.models import Thread, Message


class ChatConsumer(SyncConsumer):
    def websocket_connect(self, event):
        user = self.scope["user"]
        other_user_id = self.scope["url_route"]["kwargs"]["user_id"]
        other_user = CustomUser.objects.get(id=other_user_id)
        self.thread_obj = Thread.objects.get_or_create_personal_thread(user, other_user)
        self.room_name = f"personal_thread_{self.thread_obj.id}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name,
        )
        self.send(
            {
                "type": "websocket.accept",
            }
        )
        # self.accept()

    def websocket_receive(self, event):
        msg = json.dumps(
            {
                "sender": self.scope["user"].id,
                "text": event.get("text"),
                "thread": self.thread_obj.id,
                "created": str(timezone.now()),
                "updated": str(timezone.now()),
            },
        )

        self.store_message(event.get("text"))

        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                "type": "websocket.message",
                "text": msg,
            },
        )

    def store_message(self, text):
        Message.objects.create(
            thread=self.thread_obj,
            sender=self.scope["user"],
            text=text,
        )

    def websocket_message(self, event):
        self.send(
            {
                "type": "websocket.send",
                "text": event.get("text"),
            }
        )

    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))

    def websocket_disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name
        )
