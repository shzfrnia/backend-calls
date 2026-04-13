import uuid

from sqlmodel import Field, SQLModel


class RoleUserServer(SQLModel, table=True):
    user_server_id: uuid.UUID = Field(
        foreign_key="userserver.id", ondelete="CASCADE", primary_key=True
    )
    role_id: uuid.UUID = Field(
        foreign_key="role.id", ondelete="CASCADE", primary_key=True
    )
