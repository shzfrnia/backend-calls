import uuid

from sqlmodel import Field, SQLModel, UniqueConstraint, CheckConstraint

from app.models.mixin import CreatedMixin, OrderMixin


class UserServerBase(OrderMixin, SQLModel):
    pass


class UserServerCreate(UserServerBase):
    user_id: uuid.UUID = Field(foreign_key="user.id")
    server_id: uuid.UUID = Field(foreign_key="server.id")


class UserServer(CreatedMixin, UserServerBase, table=True):
    __table_args__ = (UniqueConstraint("user_id", "server_id", "order"),)

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    user_id: uuid.UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    server_id: uuid.UUID = Field(foreign_key="server.id", ondelete="CASCADE")


class UserServerPublic(UserServerBase):
    id: uuid.UUID
