from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.api.deps import CurrentWsUser

from app.api.manager import manager


router = APIRouter(tags=["ws"])


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    current_user: CurrentWsUser
):
    await manager.connect(websocket=websocket, user=current_user)

    while True:
        try:
            message = await websocket.receive_json()

            for client in manager.connected_clients:
                await manager.send_message(client, message)

        except WebSocketDisconnect:
            await manager.disconnect(user=current_user)
