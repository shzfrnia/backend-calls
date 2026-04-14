import uuid
from fastapi.websockets import WebSocket

from app.models.user import User
from app.models.websocket_response import WebSocketJsonResponse


class UpdateServers(WebSocketJsonResponse):
    type = "update-servers"

    def __init__(self, user):
        self.payload = {
            'servers': list(
                map(lambda x: x.model_dump(mode="json"), user.my_servers)
            )
        }


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
