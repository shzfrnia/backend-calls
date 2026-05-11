from typing import Annotated

from sqlmodel import Field, SQLModel


PasswordField = Annotated[str, Field(min_length=8, max_length=128)]


class UpdatePassword(SQLModel):
    current_password: PasswordField
    new_password: PasswordField


class CheckPassword(SQLModel):
    password: PasswordField
