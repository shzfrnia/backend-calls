from sqlmodel import Session

from app.models.user import User
from app.models.server import Server, ServerCreate
from app.models.user_server import UserServer, UserServerCreate


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

    session.add(link)
    session.commit()

    session.refresh(server)

    return server
