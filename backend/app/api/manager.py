import uuid


from fastapi.websockets import WebSocket

from sqlmodel import Session
from pydantic import TypeAdapter

from app.core.db import engine

from app.models.user import User, ChannelUser
from app.models.channel import ChannelPublic
from app.models.ws_client import WSClient
from app.models.ws.messages.update_servers import UpdateServers
from app.models.ws.message import WSMessage, UserLeftChannel, UserJoinChannel

from app.crud.server import get_server_users_by_ids


ws_message_adapter = TypeAdapter(WSMessage)


class WebSocketManager:
    def __init__(self):
        self.connected_clients: dict[str, WSClient] = {}

    def get_client(self, user: User):
        return self.connected_clients.get(str(user.id), None)

    def register_client(self, user: User, ws_client: WSClient):
        self.connected_clients[str(user.id)] = ws_client

    async def connect(self, websocket: WebSocket, user: User, mic: bool, headphones: bool):
        await websocket.accept()

        self.register_client(
            user=user,
            ws_client=WSClient(
                ws=websocket,
                user=ChannelUser(
                    **user.model_dump(),
                    mic_mute=mic, head_mute=headphones
                )
            )
        )

        await self.update_servers(user=user)

    async def update_servers(self, user: User):
        client = self.get_client(user)

        if (client):
            await client.ws.send_json(
                UpdateServers(
                    user=user, clients=self.connected_clients
                ).to_dict()
            )

    async def join_channel(self, user: ChannelUser, channel: ChannelPublic):
        user_client = self.get_client(user)
        users = self.get_server_users(channel.server_id)

        if not user_client:
            return

        if user_client.channel:
            await self.left_channel(user=user, channel=user_client.channel)

        for server_user in users:
            client = self.get_client(server_user)

            if client:
                await client.ws.send_json(
                    UserJoinChannel(
                        payload={"user": user, 'channel': channel}
                    ).model_dump(mode='json')
                )

                client.channel = channel

    async def left_channel(self, user: ChannelUser, channel: ChannelPublic):
        for server_user in self.get_server_users(channel.server_id):
            client = self.get_client(server_user)

            if client:
                await client.ws.send_json(
                    UserLeftChannel(
                        payload={"user": user, 'channel': channel}
                    ).model_dump(mode='json')
                )

                client.channel = None

    async def handle_ws_message(self, current_user: User, message: dict[str, any]):
        try:
            parsed = ws_message_adapter.validate_python(message)

            match parsed:
                case UserJoinChannel(payload=data):
                    await self.join_channel(user=data.user, channel=data.channel)

                case UserLeftChannel(payload=data):
                    await self.left_channel(user=data.user, channel=data.channel)

        except Exception as e:
            print('@@@@@@yoooy@@@@@@', e)

    def get_server_users(self, server_id: uuid.UUID):
        with Session(engine) as session:
            return get_server_users_by_ids(
                session=session,
                server_id=server_id,
                user_ids=self.connected_clients.keys()
            )

    def disconnect(self, user: User):
        del self.connected_clients[str(user.id)]


manager = WebSocketManager()
