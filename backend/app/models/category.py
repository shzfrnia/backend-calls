from typing import TYPE_CHECKING, Optional
import uuid
from sqlmodel import Field, Relationship, SQLModel

from app.models.mixin import OrderMixin


if TYPE_CHECKING:
    from app.models import Server, Channel


class CategoryBase(OrderMixin, SQLModel):
    name: str = Field(nullable=False, min_length=1, max_length=255)


class CategoryCreate(CategoryBase):
    server_id: uuid.UUID = Field(foreign_key="server.id")


class CategoryUpdate(CategoryBase):
    pass


class Category(CategoryBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    server_id: uuid.UUID = Field(
        foreign_key="server.id", nullable=False, ondelete="CASCADE"
    )
    server: Optional["Server"] = Relationship(back_populates="categories")

    channels: list["Channel"] = Relationship(
        back_populates='category',
        sa_relationship_kwargs={
            "order_by": "Channel.order"
        }
    )
