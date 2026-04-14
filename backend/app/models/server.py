from datetime import datetime
from typing import TYPE_CHECKING, Optional
import uuid

from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel

from app.utils.datetime import get_datetime_utc

from app.models.user_server import UserServer

if TYPE_CHECKING:
    from app.models import User, Role


class ServerBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)


class ServerCreate(ServerBase):
    pass


class ServerUpdate(ServerBase):
    name: str | None = Field(
        default=None, min_length=1, max_length=255
    )


class Server(ServerBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    created_at: datetime = Field(
        nullable=False,
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True)
    )

    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: Optional["User"] = Relationship(back_populates="my_servers")

    users: list["User"] = Relationship(
        back_populates="servers", link_model=UserServer,
        sa_relationship_kwargs={"passive_deletes": True}
    )

    roles: list["Role"] = Relationship(
        back_populates="servers",
        cascade_delete=True
    )


class ServerPublic(ServerBase):
    id: uuid.UUID


class ServersPublic(SQLModel):
    data: list[ServerPublic]
    count: int
