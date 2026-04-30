from typing import Literal

from pydantic import BaseModel

from .base_message import BaseWSMessage

from app.models.user import ChannelUser, UserPublic
from app.models.channel import ChannelPublic


class ChannelConnectionPayload(BaseModel):
    user: ChannelUser
    channel: ChannelPublic


class UserJoinChannelMessagePayload(ChannelConnectionPayload):
    pass


class UserJoinChannelMessage(BaseWSMessage[UserJoinChannelMessagePayload]):
    type: Literal["user-join-channel"] = "user-join-channel"


class UserJoinChannelResponse(UserJoinChannelMessage):
    pass


class UserLeftChannelMessagePayload(BaseModel):
    user: UserPublic


class UserLeftChannelMessage(BaseWSMessage[UserLeftChannelMessagePayload]):
    type: Literal["user-left-channel"] = "user-left-channel"


class UserLeftChannelResponsePayload(ChannelConnectionPayload):
    user: UserPublic


class UserLeftChannelResponse(BaseWSMessage[UserLeftChannelResponsePayload]):
    type: Literal["user-left-channel"] = "user-left-channel"
