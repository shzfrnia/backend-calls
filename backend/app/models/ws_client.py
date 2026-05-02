from dataclasses import dataclass

from fastapi.websockets import WebSocket

from app.models.user import ChannelUser
from app.models.channel import ChannelPublic


@dataclass
class WSClient:
    ws: WebSocket
    user: ChannelUser
    channel: ChannelPublic | None = None
