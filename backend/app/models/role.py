from typing import TYPE_CHECKING, Optional
import uuid

from sqlmodel import Field, Relationship, SQLModel

from app.models.role_permission import RolePermission

if TYPE_CHECKING:
    from app.models import Permission, Server


class RoleBase(SQLModel):
    name: str = Field(
        min_length=1, max_length=255,
        nullable=False, unique=True
    )


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class Role(RoleBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    permissions: list["Permission"] = Relationship(
        back_populates="roles", link_model=RolePermission
    )

    server_id: uuid.UUID = Field(
        foreign_key="server.id", nullable=False, ondelete="CASCADE"
    )
    server: Optional["Server"] = Relationship(back_populates="roles")


class RolePublic(RoleBase):
    id: uuid.UUID


class RolesPublic(SQLModel):
    data: list[RolePublic]
    count: int
