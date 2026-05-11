from typing import TYPE_CHECKING
import uuid
from datetime import datetime

from pydantic import EmailStr, computed_field
from sqlmodel import Field, Relationship, SQLModel

from app.models.user_server import UserServer
from app.models.mixin import CreatedMixin

if TYPE_CHECKING:
    from app.models import Server, Invite


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    login: str = Field(unique=True, min_length=5, max_length=255)
    nickname: str | None = Field(default=None, max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    login: str = Field(min_length=5, max_length=255)


class UserUpdate(UserBase):
    email: EmailStr | None = None


class UserUpdateMe(SQLModel):
    nickname: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


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
