import uuid


from fastapi.websockets import WebSocket

from sqlmodel import Session
from pydantic import TypeAdapter

from app.core.db import engine

from app.models.user import User, UserPublic, ChannelUser
from app.models.channel import ChannelPublic
from app.models.ws_client import WSClient
from app.models.ws.messages.update_servers import UpdateServers
from app.models.ws.messages.channels import (
    UserLeftChannelResponse, UserJoinChannelResponse, UpdateChannelUserResponse
)
from app.models.ws.message import (
    WSMessage, UserJoinChannelMessage, UserLeftChannelMessage, UserUpdateMuteMessage
)

from app.crud.server import get_server_users_by_ids, get_channel_by_id


ws_message_adapter = TypeAdapter(WSMessage)


class WebSocketManager:
    def __init__(self):
        self.connected_clients: dict[str, WSClient] = {}

    def get_client(self, user: User):
        return self.connected_clients.get(str(user.id), None)

    async def register_client(self, user: User, ws_client: WSClient):
        self.connected_clients[str(user.id)] = ws_client

    async def connect(self, websocket: WebSocket, user: User, mic: bool, headphones: bool):
        await websocket.accept()

        await self.register_client(
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

    async def join_channel(self, user: ChannelUser, channel: uuid.UUID):
        user_client = self.get_client(user)

        if not user_client:
            return

        await self.left_channel(user=user)

        with Session(engine) as session:
            channel = get_channel_by_id(
                session=session,
                channel_id=channel, user=user
            )
            if channel:
                user_client.channel = ChannelPublic(**channel.model_dump())
            else:
                return

        for server_user in self.get_server_users(user_client.channel.server_id):
            client = self.get_client(server_user)

            if client:
                await client.ws.send_json(
                    UserJoinChannelResponse(
                        payload={
                            "user": user,
                            'channel':  user_client.channel
                        }
                    ).model_dump(mode='json')
                )

    async def left_channel(self, user: UserPublic):
        user_client = self.get_client(user)

        if user_client and user_client.channel:
            for server_user in self.get_server_users(user_client.channel.server_id):
                client = self.get_client(server_user)
                if client:
                    await client.ws.send_json(
                        UserLeftChannelResponse(
                            payload={
                                "user": user,
                                'channel': user_client.channel
                            }
                        ).model_dump(mode='json')
                    )

            user_client.channel = None

    async def update_mute(self, user: User, mic: bool, head: bool):
        user_client = self.get_client(user)

        if user_client and user_client.channel:
            user_client.user.mic_mute = mic
            user_client.user.head_mute = head

            for server_user in self.get_server_users(user_client.channel.server_id):
                client = self.get_client(server_user)
                if client:
                    await client.ws.send_json(
                        UpdateChannelUserResponse(
                            payload={
                                "user": user_client.user,
                                'channel': user_client.channel
                            }
                        ).model_dump(mode='json')
                    )

    async def handle_ws_message(self, current_user: User, message: dict[str, any]):
        try:
            parsed = ws_message_adapter.validate_python(message)

            match parsed:
                case UserJoinChannelMessage(payload=data):
                    await self.join_channel(
                        user=ChannelUser(
                            **current_user.model_dump(mode='json'),
                            mic_mute=data.mute.mic,
                            head_mute=data.mute.head
                        ),
                        channel=data.channel
                    )

                case UserLeftChannelMessage(payload=data):
                    await self.left_channel(user=current_user)

                case UserUpdateMuteMessage(payload=data):
                    await self.update_mute(
                        user=current_user, mic=data.mic, head=data.head
                    )

        except Exception as e:
            print('@@@@@@yoooy@@@@@@', e)

    def get_server_users(self, server_id: uuid.UUID):
        with Session(engine) as session:
            return get_server_users_by_ids(
                session=session,
                server_id=server_id,
                user_ids=self.connected_clients.keys()
            )

    async def disconnect(self, user: User):
        client = self.get_client(user)

        if client and client.channel:
            await self.left_channel(client.user)

        del self.connected_clients[str(user.id)]


manager = WebSocketManager()
