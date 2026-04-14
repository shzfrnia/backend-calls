from typing import Any
from fastapi import APIRouter

from app.api.deps import CurrentUser, SessionDep

from app.models.server import ServerPublic, ServerCreate

from app.crud.server import create_server as create_server_fn


router = APIRouter(prefix="/servers", tags=["servers"])


@router.post("/", response_model=ServerPublic)
def create_server(
    *, session: SessionDep, current_user: CurrentUser, server_draft: ServerCreate
) -> Any:
    """
    Create new server.
    """
    return create_server_fn(session=session, user=current_user,  server_draft=server_draft)
