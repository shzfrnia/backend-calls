from fastapi import APIRouter

from app.models.system import SystemStatus

router = APIRouter(prefix="/utils", tags=["utils"])


@router.get("/health-check")
async def health_check() -> SystemStatus:
    return {"version": '0.0.1'}
