from typing import Union, Annotated
from pydantic import Field

from .messages.channels import UserJoinChannelMessage, UserLeftChannelMessage


WSMessage = Annotated[
    Union[UserJoinChannelMessage, UserLeftChannelMessage],
    Field(discriminator="type")
]
