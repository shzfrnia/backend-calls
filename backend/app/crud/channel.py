import uuid

from sqlmodel import Session, select

from app.models.user import UserPublic
from app.models.server import Server
from app.models.user_server import UserServer


from app.models.channel import Channel


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
