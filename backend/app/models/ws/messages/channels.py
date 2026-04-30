from typing import Literal

from pydantic import BaseModel

from .base_message import BaseWSMessage

from app.models.user import ChannelUser
from app.models.channel import ChannelPublic


class ChannelConnectPayload(BaseModel):
    user: ChannelUser
    channel: ChannelPublic


class UserJoinChannel(BaseWSMessage[ChannelConnectPayload]):
    type: Literal["user-join-channel"] = "user-join-channel"


class UserLeftChannel(BaseWSMessage[ChannelConnectPayload]):
    type: Literal["user-left-channel"] = "user-left-channel"
