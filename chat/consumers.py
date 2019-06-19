import json
import datetime
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chat.models import Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        if self.scope["user"].is_anonymous:
            self.close()
        else:
            self.accept()


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = str(self.scope['user'])
        now_time = datetime.datetime.now().strftime('%b %d %Y %I:%M%p')

        if not message:
            return
        if not self.scope['user'].is_authenticated:
            return
        Message.objects.create(user=self.scope['user'], message=message, group_name=self.room_group_name,created=datetime.datetime.now())
        print("__debug__",now_time)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user':user,
                'now_time':now_time,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        now_time = event['now_time']
        user = event['user']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'now_time': now_time,
        }))