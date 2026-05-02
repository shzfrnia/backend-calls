from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.api.deps import CurrentWsUser

from app.api.manager import manager


router = APIRouter(tags=["ws"])


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    current_user: CurrentWsUser,
    mic: bool = False,
    head: bool = False
):

    await manager.connect(
        websocket=websocket,
        user=current_user,
        mic=mic,
        headphones=head
    )

    try:
        while True:
            await manager.handle_ws_message(
                current_user=current_user,
                message=await websocket.receive_json()
            )

    except WebSocketDisconnect:
        await manager.disconnect(user=current_user)
