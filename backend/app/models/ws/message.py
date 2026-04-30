from typing import Union, Annotated
from pydantic import Field

from .messages.channels import (
    UserJoinChannelMessage, UserLeftChannelMessage, UserUpdateMuteMessage
)


WSMessage = Annotated[
    Union[
        UserJoinChannelMessage,
        UserLeftChannelMessage,
        UserUpdateMuteMessage
    ],
    Field(discriminator="type")
]
