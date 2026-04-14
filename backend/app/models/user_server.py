from datetime import datetime
import uuid

from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel, UniqueConstraint, CheckConstraint

from app.utils.datetime import get_datetime_utc


class UserServerBase(SQLModel):
    order: int = Field(
        nullable=False,
        ge=0,
        sa_column_args=(CheckConstraint("order > 0"),)
    )


class UserServerCreate(UserServerBase):
    user_id: uuid.UUID = Field(foreign_key="user.id")
    server_id: uuid.UUID = Field(foreign_key="server.id")


class UserServer(UserServerBase, table=True):
    __table_args__ = (UniqueConstraint("user_id", "server_id", "order"),)

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    user_id: uuid.UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    server_id: uuid.UUID = Field(foreign_key="server.id", ondelete="CASCADE")

    created_at: datetime = Field(
        nullable=False,
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True)
    )


class UserServerPublic(UserServerBase):
    id: uuid.UUID
