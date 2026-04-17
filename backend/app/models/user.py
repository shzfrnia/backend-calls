from typing import TYPE_CHECKING
import uuid
from datetime import datetime

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from app.models.user_server import UserServer
from app.models.mixin import CreatedMixin

if TYPE_CHECKING:
    from app.models import Item, Server


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    login: str = Field(unique=True, min_length=5, max_length=255)
    nickname: str | None = Field(default=None, max_length=255)
    is_active: bool = True
    is_superuser: bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    login: str | None = Field(min_length=5, max_length=255)


class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserUpdateMe(SQLModel):
    nickname: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class User(CreatedMixin, UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str

    items: list["Item"] = Relationship(
        back_populates="owner",
        cascade_delete=True
    )

    servers: list["Server"] = Relationship(
        back_populates="users", link_model=UserServer,
        sa_relationship_kwargs={"passive_deletes": True}
    )

    my_servers: list["Server"] = Relationship(back_populates="owner")


class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
