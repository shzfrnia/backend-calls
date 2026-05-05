import uuid
from typing import Any
from fastapi import APIRouter, HTTPException

from app.api.deps import CurrentUser, SessionDep
from app.api.manager import manager

from app.models.server import ServerPublic, ServerCreate
from app.models.invite import InvitePublic, InvitesPublic
from app.models.message import Message

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


@router.post("/{id}/invite")
async def invite_code(
    *, session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> InvitePublic:
    """
    Get or create invite code.
    """

    return server_crud.get_server_invite_code(
        session=session, user_id=current_user.id, server_id=id
    )


@router.get("/{id}/invites")
async def invite_code(
    *, session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> InvitesPublic:
    """
    Get or create invite code.
    """
    result = server_crud.get_server_invites(
        session=session, user_id=current_user.id, server_id=id
    )

    return InvitesPublic(data=result, count=len(result))


@router.delete("/{id}/invite/{invite_id}")
async def delete_invite(
    *, session: SessionDep, current_user: CurrentUser, id: uuid.UUID, invite_id: uuid.UUID
) -> Message:
    """
    Delete invite code.
    """
    server_crud.delete_server_invite(
        session=session,
        user_id=current_user.id,
        server_id=id,
        invite_id=invite_id
    )

    return Message(message="Invite deleted successfully")


@router.delete("/{id}/invites")
async def delete_invite(
    *, session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete invite code.
    """
    server_crud.delete_server_invites(
        session=session,
        user_id=current_user.id,
        server_id=id,
    )

    return Message(message="Invites deleted successfully")
