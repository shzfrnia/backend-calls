from typing import TYPE_CHECKING, Optional
import uuid

from sqlmodel import Field, Relationship, SQLModel, CheckConstraint


from app.models.mixin import CreatedMixin

if TYPE_CHECKING:
    from app.models import Server, User
    from app.models.user import UserPublic


class InviteBase(SQLModel):
    pass


class InviteCreate(InviteBase):
    pass


class Invite(CreatedMixin, InviteBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    used: int = Field(
        default=0,
        nullable=False,
        ge=0,
        sa_column_args=(CheckConstraint("used > 0"),)
    )

    code: str = Field(
        min_length=1, max_length=255,
        nullable=False, unique=True
    )

    server_id: uuid.UUID = Field(
        foreign_key="server.id", nullable=False, ondelete="CASCADE"
    )
    server: Optional["Server"] = Relationship(back_populates="invites")

    user_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    user: Optional["User"] = Relationship(back_populates="invites")


class InvitePublic(InviteBase):
    id: uuid.UUID
    used: int
    code: str
    user: "UserPublic"


class InvitesPublic(SQLModel):
    data: list["InvitePublic"]
    count: int


from app.models.user import UserPublic  # noqa

InvitePublic.model_rebuild()
InvitesPublic.model_rebuild()
