import uuid
import secrets
import string

from sqlmodel import Session, select, col, delete
from sqlalchemy.orm import selectinload

from app.models.user import User, UserPublic
from app.models.server import Server, ServerCreate
from app.models.user_server import UserServer, UserServerCreate

from app.models.category import Category, CategoryCreate
from app.models.channel import Channel, ChannelCreate
from app.models.invite import Invite


def create_server(*, session: Session, user: User, server_draft: ServerCreate) -> Server:
    server = Server.model_validate(server_draft, update={"owner_id": user.id})

    session.add(server)
    session.commit()
    session.refresh(server)

    link = UserServer.model_validate(
        UserServerCreate(
            user_id=user.id,
            server_id=server.id,
            order=len(user.servers) + 1
        )
    )

    category1 = Category.model_validate(
        CategoryCreate(order=0, name="Голосовые каналы 1", server_id=server.id)
    )
    session.add(category1)
    category2 = Category.model_validate(
        CategoryCreate(order=2, name="Голосовые каналы 2", server_id=server.id)
    )
    session.add(category2)
    session.commit()
    session.refresh(category1)
    session.refresh(category2)

    channel1 = Channel.model_validate(
        ChannelCreate(
            order=1, name="Голосовой канал с очень длинным именем",
            category_id=category1.id
        ),
        update={"server_id": server.id}
    )
    session.add(channel1)
    channel2 = Channel.model_validate(
        ChannelCreate(
            order=3, name="Голосовой канал 1",
            category_id=category2.id
        ),
        update={"server_id": server.id}
    )
    session.add(channel2)
    channel3 = Channel.model_validate(
        ChannelCreate(
            order=4, name="Голосовой канал 2", limit=69,
            category_id=category2.id
        ),
        update={"server_id": server.id}
    )
    session.add(channel3)

    channel = Channel.model_validate(
        ChannelCreate(order=5, name="Голосовой канал 3"),
        update={"server_id": server.id}
    )
    session.add(channel)

    session.add(link)
    session.commit()

    session.refresh(server)

    return server


def delete_server(*, session: Session, user: User, id: uuid.UUID) -> bool:
    server = session.get(Server, id)
    if not server:
        raise ValueError("Item not found")
    if user.id != server.owner_id:
        raise PermissionError(detail="Not enough permissions")

    session.delete(server)
    session.commit()

    return True


def get_user_with_servers_tree(*, session: Session, user_id: uuid.UUID):
    statement = (
        select(User)
        .where(User.id == user_id)
        .options(
            # selectinload(User.servers)
            # .selectinload(Server.users),

            selectinload(User.servers)
            .selectinload(Server.categories),

            selectinload(User.servers)
            .selectinload(Server.categories)
            .selectinload(Category.channels),

            selectinload(User.servers)
            .selectinload(Server.channels)
        )
    )

    result = session.exec(statement)

    return result.one_or_none()


def get_server_users_by_ids(*, session: Session, server_id: uuid.UUID, user_ids: list[uuid.UUID]):
    statement = (
        select(User)
        .join(UserServer)
        .where(UserServer.server_id == server_id)
        .where(col(UserServer.user_id).in_(user_ids))
    )

    result = session.exec(statement)

    return result.all()


def get_channel_by_id(*, session: Session, channel_id: uuid.UUID, user: UserPublic):
    statement = (
        select(Channel)
        .join(Server)
        .join(UserServer)
        .where(UserServer.user_id == user.id)
        .where(Channel.id == channel_id)
    )

    result = session.exec(statement)

    return result.one_or_none()


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
        raise ValueError('User not member')

    statement = (
        select(Invite)
        .join(Server)
        .where(Server.id == server_id).where(Invite.user_id == user_id)
    )
    invite = session.exec(statement).one_or_none()

    if invite:
        return invite
    characters = string.digits
    code = '-'.join(
        ''.join(secrets.choice(characters) for __ in range(4))
        for _ in range(3)
    )
    invite = Invite(server_id=server_id, user_id=user_id, code=code)
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
        raise ValueError('User not member')

    if (not server_user.server.owner_id == user_id):
        raise ValueError('Permission')

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
        raise ValueError('User not member')

    if (not server_user.server.owner_id == user_id):
        raise ValueError('Permission')

    invite = session.get(Invite, invite_id)
    if not invite:
        raise ValueError("Invite not found")

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
        raise ValueError('User not member')

    if (not server_user.server.owner_id == user_id):
        raise ValueError('Permission')

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
    invite = session.exec(
        (select(Invite).where(Invite.code == code))
    ).one_or_none()

    if not invite:
        raise ValueError('Server not found')

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


def leave_from_server(*, session: Session, server_id: str, user: User):
    statement = (
        select(UserServer)
        .where(
            UserServer.server_id == server_id,
            UserServer.user_id == user.id
        )
    )

    link = session.exec(statement).one_or_none()

    if link:
        session.delete(link)
        session.commit()
    else:
        raise ValueError('link not found')

    return True
