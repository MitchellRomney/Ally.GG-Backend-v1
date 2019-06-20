from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class UserConsumer(WebsocketConsumer):
    def connect(self):
        self.userId = self.scope['url_route']['kwargs']['userId']
        self.room_group_name = 'dashboard_%s' % self.userId

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def celery(self, event):
        message = event['message']
        data = event['data'] if 'data' in event else None

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'data': data
        }))


class SummonerConsumer(WebsocketConsumer):
    def connect(self):
        self.summoner = self.scope['url_route']['kwargs']['summonerName']
        self.room_group_name = 'summoner_%s' % self.summoner

        print(self.room_group_name)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def celery(self, event):
        message = event['message']
        data = event['data'] if 'data' in event else None

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'data': data
        }))
