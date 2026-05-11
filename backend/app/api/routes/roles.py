import uuid

from fastapi import APIRouter

from app.api.deps import SessionDep, CurrentUser

from app.models.role import RolesPublic

router = APIRouter(tags=["roles"])


@router.get("/servers/{server_id}/roles", response_model=RolesPublic)
def server_roles(*, session: SessionDep, current_user: CurrentUser, server_id: uuid.UUID) -> RolesPublic:
    return RolesPublic(data=[], count=0)
