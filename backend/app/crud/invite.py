import uuid
import secrets
import string


from sqlmodel import Session, select, delete

from app.errors import AccessDeniedError, ObjectNotFoundError

from app.models.user import User
from app.models.server import Server
from app.models.user_server import UserServer, UserServerCreate


from app.models.invite import Invite


def get_server_invite_code(*, session: Session, server_id: uuid.UUID, user_id: uuid.UUID):
    statement = (
        select(UserServer)
        .where(
            UserServer.user_id == user_id,
            UserServer.server_id == server_id
        )
    )
    user_is_member = session.exec(statement)

    if (not user_is_member.one_or_none()):
        raise AccessDeniedError('User not member')

    statement = (
        select(Invite)
        .where(
            Invite.server_id == server_id,
            Invite.owner_id == user_id
        )
    )
    invite = session.exec(statement).one_or_none()

    if invite:
        return invite

    characters = string.digits
    invite = Invite(
        server_id=server_id,
        owner_id=user_id,
        code='-'.join(
            ''.join(secrets.choice(characters) for __ in range(4))
            for _ in range(3)
        )
    )

    session.add(invite)
    session.commit()
    session.refresh(invite)

    return invite


def get_server_invites(*, session: Session, server_id: uuid.UUID, user_id: uuid.UUID):
    statement = (
        select(UserServer)
        .where(
            UserServer.user_id == user_id,
            UserServer.server_id == server_id
        )
    )
    server_user = session.exec(statement).one_or_none()

    if (not server_user):
        raise AccessDeniedError('User not member')

    if (not server_user.server.owner_id == user_id):
        raise AccessDeniedError()

    return server_user.server.invites


def delete_server_invite(
        *, session: Session, server_id: uuid.UUID, user_id: uuid.UUID, invite_id: uuid.UUID
):
    statement = (
        select(UserServer)
        .where(
            UserServer.user_id == user_id,
            UserServer.server_id == server_id
        )
    )
    server_user = session.exec(statement).one_or_none()

    if (not server_user):
        raise AccessDeniedError('User not member')

    if (not server_user.server.owner_id == user_id):
        raise AccessDeniedError()

    invite = session.get(Invite, invite_id)
    if not invite:
        raise ObjectNotFoundError("Invite not found")

    session.delete(invite)
    session.commit()

    return True


def delete_server_invites(
        *, session: Session, server_id: uuid.UUID, user_id: uuid.UUID
):
    statement = (
        select(UserServer)
        .where(
            UserServer.user_id == user_id,
            UserServer.server_id == server_id
        )
    )
    server_user = session.exec(statement).one_or_none()

    if (not server_user):
        raise AccessDeniedError('User not member')

    if (not server_user.server.owner_id == user_id):
        raise AccessDeniedError()

    statement = (
        delete(Invite)
        .where(Invite.server_id == server_id)
    )

    session.exec(statement)
    session.commit()

    return True


def get_server_by_code(*, session: Session, code: str):
    statement = (select(Server).join(Invite).where(Invite.code == code))
    return session.exec(statement).one_or_none()


def join_user_to_server_by_code(*, session: Session, code: str, user: User):
    statement = select(Invite).where(Invite.code == code)
    invite = session.exec(statement).one_or_none()

    if not invite:
        raise ObjectNotFoundError('Server not found')

    server = invite.server

    link = UserServer.model_validate(
        UserServerCreate(
            user_id=user.id,
            server_id=server.id,
            order=len(user.servers) + 1
        )
    )

    invite.used = invite.used + 1

    session.add(invite)
    session.add(link)
    session.commit()

    return True
