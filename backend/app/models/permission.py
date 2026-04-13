from typing import TYPE_CHECKING
import uuid

from sqlmodel import Field, Relationship, SQLModel

from app.models.role_permission import RolePermission

if TYPE_CHECKING:
    from app.models import Role


class PermissionBase(SQLModel):
    name: str = Field(min_length=1, max_length=255, nullable=False)


class Permission(PermissionBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    roles: list["Role"] = Relationship(
        back_populates="permissions", link_model=RolePermission
    )
