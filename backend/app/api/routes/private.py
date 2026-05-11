from typing import Any

from fastapi import APIRouter

from app.api.deps import SessionDep


router = APIRouter(tags=["private"], prefix="/test")


@router.post("/")
def test(session: SessionDep) -> Any:
    """
    Test
    """
    return []
