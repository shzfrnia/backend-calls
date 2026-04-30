from typing import Union, Annotated
from pydantic import Field

from .messages.channels import UserJoinChannel, UserLeftChannel


WSMessage = Annotated[
    Union[UserJoinChannel, UserLeftChannel],
    Field(discriminator="type")
]
