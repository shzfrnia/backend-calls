import json
from typing import Annotated

import sentry_sdk
from fastapi import Depends, FastAPI, Query, WebSocket
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.api.deps import CurrentWsUser
from app.core.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)


# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=settings.all_cors_origins,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


class WebSocketJsonResponse:
    def __init__(self, type: str, payload):
        self.type = type
        self.payload = payload

    def to_dict(self):
        return {"type": self.type, "payload": self.payload}


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    current_user: CurrentWsUser
):
    await websocket.accept()

    await websocket.send_json(
        WebSocketJsonResponse(
            'update-application-data',
            {
                "servers": list(map(lambda x: x.model_dump(mode="json"), current_user.my_servers))
            }
        ).to_dict()
    )

    while True:
        await websocket.receive_text()

    # while True:
    #     data = await websocket.receive_text()
    #     await websocket.send_text(f"Message text was: {data}")
