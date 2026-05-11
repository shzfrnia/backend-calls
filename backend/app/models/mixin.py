import uuid
from datetime import datetime

from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel, CheckConstraint

from app.utils.datetime import get_datetime_utc


class OrderMixin(SQLModel):
    order: int = Field(
        nullable=False,
        ge=0,
        sa_column_args=(CheckConstraint("order > 0"),)
    )


class CreatedMixin(SQLModel):
    created_at: datetime = Field(
        nullable=False,
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True)
    )


class UUIDMixin(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
