import itertools
import json

from sqlmodel import Session

from app.core.db import engine

from app.models.user import User
from app.models.server import Server
from app.models.channel import Channel
from app.models.category import Category
from app.models.ws.response import WebSocketJsonResponse
from app.models.ws_client import WSClient

from app.crud.server import get_user_with_servers_tree


class UpdateServers(WebSocketJsonResponse):
    type = "update-servers"

    def __init__(self, user: User, clients: dict[str, WSClient]):
        self.clients = clients

        with Session(engine) as session:
            servers = map(
                self.transform_server,
                get_user_with_servers_tree(
                    session=session, user_id=user.id
                ).servers
            )

        self.payload = {'servers': list(servers)}

    def transform_server(self, server: Server):
        return {
            **server.model_dump(mode='json'),
            'channels': self.build_channels_tree(server=server),
            "users": {
                id: {
                    **client.user.model_dump(mode='json'),
                    'channel': client.channel.model_dump(mode='json', include=('id', 'name'))
                }
                for (id, client) in self.clients.items()
                if client.channel and str(client.channel.server_id) == str(server.id)
            }
        }

    def transform_category(self, category: Category):
        return {
            **category.model_dump(mode='json'),
            'channels': list(map(self.transform_channel, category.channels))
        }

    def transform_channel(self, channel: Channel):
        json_data = channel.model_dump(mode='json')
        json_data['settings'] = {
            'limit': json_data.pop('limit', 0)
        }

        return json_data

    def build_channels_tree(self, server: Server):
        categories = map(self.transform_category, server.categories)

        withoutCategory = map(
            self.transform_channel,
            (ch for ch in server.channels if ch.category_id is None)
        )

        return sorted(
            itertools.chain(categories, withoutCategory),
            key=lambda x: x["order"]
        )
