from typing import TYPE_CHECKING, Optional
import uuid
from datetime import datetime

from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel


from app.utils.datetime import get_datetime_utc


if TYPE_CHECKING:
    from app.models.user import User


# Shared properties
class ServerBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    icon: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ServerCreate(ServerBase):
    pass


# Properties to receive on item update
class ServerUpdate(ServerBase):
    name: str | None = Field(
        default=None, min_length=1, max_length=255
    )
    icon: str | None = Field(
        default=None, min_length=1, max_length=255
    )


# Database model, database table inferred from class name
class Server(ServerBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: Optional["User"] = Relationship(back_populates="servers")


# Properties to return via API, id is always required
class ServerPublic(ServerBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime | None = None


class ServerPublic(SQLModel):
    data: list[ServerPublic]
    count: int
