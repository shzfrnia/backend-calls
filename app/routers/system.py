from fastapi import APIRouter, Path
from pydantic import BaseModel

router = APIRouter(tags=['system'])


class SystemStatus(BaseModel):
    version: str


@router.get("/check", summary='SystemStatus', description='Check system status')
async def read_users() -> SystemStatus:
    return {"version": '0.0.1'}
