import uuid

from sqlmodel import Session, select, col
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.models.server import Server, ServerCreate
from app.models.user_server import UserServer, UserServerCreate

from app.models.category import Category, CategoryCreate
from app.models.channel import Channel, ChannelCreate


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
