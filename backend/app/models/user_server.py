from datetime import datetime
import uuid

from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel, UniqueConstraint

from app.utils.datetime import get_datetime_utc


class UserServerBase(SQLModel):
    pass


class UserServer(UserServerBase, table=True):
    __table_args__ = (UniqueConstraint("user_id", "server_id"),)

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
    created_at: datetime
