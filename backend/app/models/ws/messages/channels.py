from typing import Literal
import uuid

from pydantic import BaseModel

from .base_message import BaseWSMessage

from app.models.user import ChannelUser, UserPublic
from app.models.channel import ChannelPublic


class Mute(BaseModel):
    mic: bool
    head: bool


class UserJoinChannelMessagePayload(BaseModel):
    channel: uuid.UUID
    mute: Mute


class UserJoinChannelMessage(BaseWSMessage[UserJoinChannelMessagePayload]):
    type: Literal["user-join-channel"] = "user-join-channel"


class UserJoinChannelResponsePayload(BaseModel):
    channel: ChannelPublic
    user: ChannelUser


class UserJoinChannelResponse(BaseWSMessage[UserJoinChannelResponsePayload]):
    type: Literal["user-left-channel"] = "user-join-channel"


class UserLeftChannelMessagePayload(BaseModel):
    user: UserPublic


class UserLeftChannelMessage(BaseWSMessage[UserLeftChannelMessagePayload]):
    type: Literal["user-left-channel"] = "user-left-channel"
    payload: None = None


class UserLeftChannelResponsePayload(BaseModel):
    channel: ChannelPublic
    user: UserPublic


class UserLeftChannelResponse(BaseWSMessage[UserLeftChannelResponsePayload]):
    type: Literal["user-left-channel"] = "user-left-channel"


class UserUpdateMuteMessagePayload(BaseModel):
    mic: bool
    head: bool


class UserUpdateMuteMessage(BaseWSMessage[UserUpdateMuteMessagePayload]):
    type: Literal["user-update-mute"] = "user-update-mute"


class UpdateChannelUserResponsePayload(BaseModel):
    channel: ChannelPublic
    user: ChannelUser


class UpdateChannelUserResponse(BaseWSMessage[UpdateChannelUserResponsePayload]):
    type: Literal["update-channel-user"] = "update-channel-user"
