from typing import TYPE_CHECKING, Optional
import uuid

from sqlmodel import Field, Relationship, SQLModel

from app.models.mixin import OrderMixin


if TYPE_CHECKING:
    from app.models import Server, Category


class ChannelBase(OrderMixin, SQLModel):
    name: str = Field(nullable=False, min_length=1, max_length=255)
    limit: int = Field(default=0, ge=0, le=100, nullable=False)

    category_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="category.id"
    )


class ChannelCreate(ChannelBase):
    pass


class ChannelUpdate(ChannelBase):
    pass


class Channel(ChannelBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    server_id: uuid.UUID = Field(
        foreign_key="server.id", nullable=False, ondelete="CASCADE"
    )
    server: Optional["Server"] = Relationship(back_populates="channels")

    category_id: Optional[uuid.UUID] = Field(
        foreign_key="category.id", nullable=True, ondelete="CASCADE"
    )
    category: Optional["Category"] = Relationship(back_populates="channels")


class ChannelPublic(ChannelBase):
    id: uuid.UUID
    server_id: uuid.UUID
