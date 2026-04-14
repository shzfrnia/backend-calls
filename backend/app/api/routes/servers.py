from typing import Any
from fastapi import APIRouter

from app.api.deps import CurrentUser, SessionDep
from app.api.manager import manager

from app.models.server import ServerPublic, ServerCreate

import app.crud.server as server_crud


router = APIRouter(prefix="/servers", tags=["servers"])


@router.post("/", response_model=ServerPublic)
async def create_server(
    *, session: SessionDep, current_user: CurrentUser, server_draft: ServerCreate
) -> Any:
    """
    Create new server.
    """
    server = server_crud.create_server(
        session=session, user=current_user,  server_draft=server_draft
    )

    await manager.update_servers(user=current_user)

    return server
