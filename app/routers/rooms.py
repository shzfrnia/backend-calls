from fastapi import APIRouter, Path
from pydantic import BaseModel

router = APIRouter(prefix="/room", tags=['rooms'])


class Room(BaseModel):
    room: str


@router.get("/{room}", summary='Rooms', description='Room of users')
async def read_users(room: str = Path(
        title='Room ID',
        description='Room ID',
        example="71b2e4ba-b0b0-42a0-b8d6-22af3b885368")) -> Room:
    return {"room": room}
