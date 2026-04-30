from typing import TYPE_CHECKING, Optional
import uuid

from sqlmodel import Field, Relationship, SQLModel

from app.models.user_server import UserServer
from app.models.mixin import CreatedMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models import Role, Category, Channel


class ServerBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)


class ServerCreate(ServerBase):
    pass


class ServerUpdate(ServerBase):
    name: str | None = Field(
        default=None, min_length=1, max_length=255
    )


class Server(CreatedMixin, ServerBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: Optional["User"] = Relationship(back_populates="my_servers")

    users: list["User"] = Relationship(
        back_populates="servers", link_model=UserServer,
        sa_relationship_kwargs={"passive_deletes": True}
    )

    roles: list["Role"] = Relationship(
        back_populates="server",
        cascade_delete=True
    )

    categories: list["Category"] = Relationship(
        back_populates='server',
        cascade_delete=True,
        sa_relationship_kwargs={
            "order_by": "Category.order"
        }
    )

    channels: list["Channel"] = Relationship(
        back_populates='server',
        cascade_delete=True,
        sa_relationship_kwargs={
            "order_by": "Channel.order"
        }
    )


class ServerPublic(ServerBase):
    id: uuid.UUID


class ServersPublic(SQLModel):
    data: list[ServerPublic]
    count: int
