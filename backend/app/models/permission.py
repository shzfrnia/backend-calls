from typing import TYPE_CHECKING, Annotated

from sqlmodel import Field, Relationship, SQLModel

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


class Permission(PermissionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    roles: list["Role"] = Relationship(
        back_populates="permissions", link_model=RolePermission
    )


class PermissionPublic(PermissionBase):
    id: int
