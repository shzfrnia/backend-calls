from typing import TYPE_CHECKING, Annotated
import uuid

from sqlmodel import Field, Relationship, SQLModel

from app.models.mixin import UUIDMixin
from app.models.role_permission import RolePermission


if TYPE_CHECKING:
    from app.models import Role


PermissionField = Annotated[
    str,
    Field(min_length=1, max_length=255, nullable=False)
]


class PermissionBase(SQLModel):
    subject: PermissionField
    name: PermissionField


class Permission(UUIDMixin, PermissionBase, table=True):
    roles: list["Role"] = Relationship(
        back_populates="permissions", link_model=RolePermission
    )


class PermissionPublic(PermissionBase):
    id: uuid.UUID
