from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


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

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    def celery(self, event):
        message = event['message']
        data = event['data'] if 'data' in event else None

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'data': data
        }))
