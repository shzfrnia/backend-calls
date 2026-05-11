import uuid
from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUser, SessionDep

from app.api.manager import manager

from app.models.server import ServerPublic
from app.models.invite import InvitePublic, InvitesPublic
from app.models.message import Message

from app.crud import invite as invite_crud


router = APIRouter(tags=["invites"])


@router.post("/servers/{server_id}/invites", response_model=InvitePublic)
def get_or_create_server_invite(
    *, session: SessionDep, current_user: CurrentUser, server_id: uuid.UUID
) -> InvitePublic:
    """
    Get or create invite code.
    """

    return invite_crud.get_server_invite_code(
        session=session, user_id=current_user.id, server_id=server_id
    )


@router.get("/servers/{server_id}/invites", response_model=InvitesPublic)
def server_invites(
    *, session: SessionDep, current_user: CurrentUser, server_id: uuid.UUID
) -> InvitesPublic:
    """
    Get all server invites.
    """
    result = invite_crud.get_server_invites(
        session=session, user_id=current_user.id, server_id=server_id
    )

    return InvitesPublic(data=result, count=len(result))


@router.delete("/servers/{server_id}/invites/{invite_id}", response_model=Message)
def delete_server_invite(
    *, session: SessionDep, current_user: CurrentUser, server_id: uuid.UUID, invite_id: uuid.UUID
) -> Message:
    """
    Delete server invite.
    """
    invite_crud.delete_server_invite(
        session=session,
        user_id=current_user.id,
        server_id=server_id,
        invite_id=invite_id
    )

    return Message(message="Invite deleted successfully")


@router.delete("/servers/{server_id}/invites", response_model=Message)
def delete_server_invites(
    *, session: SessionDep, current_user: CurrentUser, server_id: uuid.UUID
) -> Message:
    """
    Delete all server invites.
    """
    invite_crud.delete_server_invites(
        session=session,
        user_id=current_user.id,
        server_id=server_id,
    )

    return Message(message="Invites deleted successfully")


@router.get("/servers/invites/{code}", response_model=ServerPublic)
async def get_server_by_invite(
    *, session: SessionDep, current_user: CurrentUser, code: str
) -> ServerPublic:
    """
    Get server by invite code
    """
    server = invite_crud.get_server_by_code(session=session, code=code)

    if not server:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ServerPublic(**server.model_dump())


@router.post("/servers/invites/{code}", response_model=Message)
async def join_server_by_invite(
    *, session: SessionDep, current_user: CurrentUser, code: str
) -> Message:
    """
    Join server by code
    """
    invite_crud.join_user_to_server_by_code(
        session=session, user=current_user, code=code
    )

    await manager.update_servers(user=current_user)

    return Message(message="Joined")
