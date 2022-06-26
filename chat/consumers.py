"""Chat consumers."""

import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    """Handle asynch connection via websocket."""

    async def connect(self):
        """Handle client connection."""
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join to room
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Handle client disconnection."""
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, data):
        """Receive client info."""
        data = json.loads(data)

        # Send message to room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'name': data['name'],
                'text': data['text'],
            },
        )

    async def chat_message(self, event):
        """Receive room info."""

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    'type': 'chat_message',
                    'name': event['name'],
                    'text': event['text'],
                }
            )
        )
