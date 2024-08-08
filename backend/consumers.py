# backend/consumers.py
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

socket_logger = logging.getLogger("socket")

class EventConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.event_id = self.scope['url_route']['kwargs']['event_id']
        self.event_group_name = f'event_{self.event_id}'

        socket_logger.info(f'Connecting to WebSocket: event_id={self.event_id}, event_group_name={self.event_group_name}')

        # Join event group
        await self.channel_layer.group_add(
            self.event_group_name,
            self.channel_name
        )

        await self.accept()
        socket_logger.info(f'Successfully connected to WebSocket: event_id={self.event_id}')

    async def disconnect(self, close_code):
        socket_logger.info(f'Disconnecting from WebSocket: event_id={self.event_id}, close_code={close_code}')

        # Leave event group
        await self.channel_layer.group_discard(
            self.event_group_name,
            self.channel_name
        )

        socket_logger.info(f'Successfully disconnected from WebSocket: event_id={self.event_id}')

    async def receive(self, text_data):
        socket_logger.info(f'Received message on WebSocket: event_id={self.event_id}, message={text_data}')

        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to event group
        await self.channel_layer.group_send(
            self.event_group_name,
            {
                'type': 'event_message',
                'message': message
            }
        )

    async def event_message(self, event):
        message = event['message']
        socket_logger.info(f'Sending message to WebSocket: event_id={self.event_id}, message={message}')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))