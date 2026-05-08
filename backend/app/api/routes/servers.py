import uuid
from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUser, SessionDep
from app.api.manager import manager

from app.models.server import ServerPublic, ServerCreate
from app.models.message import Message

import app.crud.server as server_crud


router = APIRouter(prefix="/servers", tags=["servers"])


@router.post("/", response_model=ServerPublic)
async def create_server(
    *, session: SessionDep, current_user: CurrentUser, server_draft: ServerCreate
) -> ServerPublic:
    """
    Create new server.
    """
    server = server_crud.create_server(
        session=session, user=current_user,  server_draft=server_draft
    )

    await manager.update_servers(user=current_user)

    return server


@router.delete("/{id}")
async def delete_server(
    *, session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete server.
    """
    try:
        server_crud.delete_server(session=session, user=current_user, id=id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Server not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    await manager.update_servers(user=current_user)

    return Message(message="Server deleted successfully")


@router.post("/{id}/leave")
async def leave_from_server(
    *, session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Join server by code
    """
    try:
        server_crud.leave_from_server(
            session=session, user=current_user, server_id=id
        )
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    client = manager.get_client(user=current_user)
    if client.channel and client.channel.server_id == id:
        await manager.left_channel(user=current_user)
    await manager.update_servers(user=current_user)

    return Message(message="Success")
