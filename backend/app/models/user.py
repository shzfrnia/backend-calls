from typing import TYPE_CHECKING, Annotated
import uuid
from datetime import datetime

from pydantic import EmailStr, computed_field
from sqlmodel import Field, Relationship, SQLModel

from app.models.user_server import UserServer
from app.models.password import PasswordField
from app.models.mixin import CreatedMixin

if TYPE_CHECKING:
    from app.models import Server, Invite


LoginField = Annotated[
    str,
    Field(unique=True, min_length=5, max_length=255, index=True)
]
EmailField = Annotated[
    EmailStr,
    Field(unique=True, index=True, max_length=255)
]
NicknameField = Annotated[
    str | None,
    Field(default=None, max_length=255)
]


class UserBase(SQLModel):
    email: EmailField
    login: LoginField
    nickname: NicknameField


class UserCreate(UserBase):
    password: PasswordField


class UserRegister(SQLModel):
    email: EmailField
    password: PasswordField
    login: LoginField


class UserUpdateMe(SQLModel):
    nickname: NicknameField
    email: EmailField | None


class User(CreatedMixin, UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    hashed_password: str

    is_active: bool = True
    is_superuser: bool = False

    servers: list["Server"] = Relationship(
        back_populates="users", link_model=UserServer,
        sa_relationship_kwargs={
            "passive_deletes": True,
            "order_by": "UserServer.order"
        }
    )
    user_servers: list["UserServer"] = Relationship(back_populates='user')

    my_servers: list["Server"] = Relationship(back_populates="owner")

    invites: list["Invite"] = Relationship(back_populates='owner')


class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime

    @computed_field
    def display_name(self) -> str:
        return self.nickname or self.login


class ChannelUser(UserPublic):
    mic_mute: bool
    head_mute: bool


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
