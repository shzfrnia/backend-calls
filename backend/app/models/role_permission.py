import uuid

from sqlmodel import Field, SQLModel


class RolePermission(SQLModel, table=True):
    role_id: uuid.UUID = Field(
        foreign_key="role.id", ondelete="CASCADE", primary_key=True
    )
    permission_id: uuid.UUID = Field(
        foreign_key="permission.id", ondelete="CASCADE", primary_key=True
    )
