import itertools
import json

from fastapi.websockets import WebSocket

from app.models.user import User
from app.models.server import Server
from app.models.channel import Channel
from app.models.category import Category
from app.models.websocket_response import WebSocketJsonResponse


class UpdateServers(WebSocketJsonResponse):
    type = "update-servers"

    def __init__(self, user: User):
        servers = map(self.transform_server, user.servers)

        self.payload = {'servers': list(servers)}

        # print(json.dumps(self.payload, indent=4, ensure_ascii=False))

    def transform_server(self, server: Server):
        return {
            **server.model_dump(mode='json'),
            'channels': self.build_channels_tree(server=server)
        }

    def transform_category(self, category: Category):
        return {
            **category.model_dump(mode='json'),
            'channels': []
        }

    def transform_channel(self, channel: Channel):
        json_data = channel.model_dump(mode='json')
        json_data['settings'] = {
            'limit': json_data.pop('limit', 0)
        }

        return json_data

    def build_channels_tree(self, server: Server):
        categories = {
            ch['id']: ch for ch in map(
                self.transform_category, server.categories
            )
        }

        inCategory, withoutCategory = [], []
        for ch in map(self.transform_channel, server.channels):
            (inCategory if ch["category_id"] else withoutCategory).append(ch)

        for key, group in itertools.groupby(
            sorted(inCategory, key=lambda x: x['category_id']), key=lambda x: x["category_id"]
        ):
            categories[key]['channels'] = list(group)

        return sorted(
            itertools.chain(categories.values(), withoutCategory),
            key=lambda x: x["order"]
        )


class WebSocketManager:
    def __init__(self):
        self.connected_clients: dict[str, WebSocket] = {}

    def get_ws(self, user: User):
        return self.connected_clients[str(user.id)]

    def set_ws(self, user: User, websocket: WebSocket):
        self.connected_clients[str(user.id)] = websocket

    async def connect(self, websocket: WebSocket, user: User):
        await websocket.accept()

        self.set_ws(user=user, websocket=websocket)

        await self.update_servers(user=user)

    async def update_servers(self, user: User):
        ws = self.get_ws(user=user)

        if (ws):
            await ws.send_json(UpdateServers(user=user).to_dict())

    async def send_message(self, websocket: WebSocket, message: dict):
        message = {
            "client": message['client'],
            "message": message['content'],
            "timestamp": message['timestamp']
        }

        await websocket.send_json(message)

    async def disconnect(self, user: User):
        del self.connected_clients[str(user.id)]


manager = WebSocketManager()
