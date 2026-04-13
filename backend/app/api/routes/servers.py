from typing import Any
from fastapi import APIRouter

from app.api.deps import CurrentUser, SessionDep

from app.models.server import Server, ServerPublic, ServerCreate

router = APIRouter(prefix="/servers", tags=["servers"])


@router.post("/", response_model=ServerPublic)
def create_server(
    *, session: SessionDep, current_user: CurrentUser, item_in: ServerCreate
) -> Any:
    """
    Create new server.
    """
    server = Server.model_validate(
        item_in, update={"owner_id": current_user.id}
    )
    session.add(server)
    session.commit()
    session.refresh(server)
    return server
