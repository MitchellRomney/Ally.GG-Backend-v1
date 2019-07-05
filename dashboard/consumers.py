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

        summoner_id = self.scope['url_route']['kwargs']['summonerId']
        server = self.scope['url_route']['kwargs']['server']

        self.room_group_name = 'summoner_{0}_{1}'.format(server, summoner_id)

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


class AdminConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            'admin_panel',
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            'admin_panel',
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