
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uuid

from .routers import system


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = '/api'

app.include_router(prefix=API_PREFIX, router=system.router)


@app.get("/")
def root():
    return {"Hello": "app"}


response = {
    "servers": [
        {
            "id": str(uuid.uuid4()),
            "name": "Девичий цитатник",
            "icon": 'cat',
            "channels": [
                {"id": str(uuid.uuid4()), "name": "Test room"}
            ]},
        {
            "id": str(uuid.uuid4()),
            "name": "BANDA",
            "icon": 'bird',
            "channels": [
                {"id": str(uuid.uuid4()), "name": "Test room"}
            ]},
        {
            "id": str(uuid.uuid4()),
            "name": "ТОКСИКИ",
            "icon": 'panda',
            "channels": [
                {"id": str(uuid.uuid4()), "name": "Test room"}
            ]
        },
    ]
}

response2 = {
    "servers": [
        {
            "id": str(uuid.uuid4()),
            "name": "Девичий цитатник",
            "icon": 'cat',
            "channels": [
                {"id": str(uuid.uuid4()), "name": "Test room"}
            ]},
        {
            "id": str(uuid.uuid4()),
            "name": "BANDA",
            "icon": 'bird',
            "channels": [
                {"id": str(uuid.uuid4()), "name": "Test room"}
            ]},

    ]
}


class WebSocketJsonResponse:
    def __init__(self, type: str, payload):
        self.type = type
        self.payload = payload

    def to_dict(self):

        return {"type": self.type, "payload": self.payload}


@app.websocket("/ws")  # add user token
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json(WebSocketJsonResponse('update-application-data', response).to_dict())
    # await asyncio.sleep(2)
    # await websocket.send_json(WebSocketJsonResponse('update-application-data', response2).to_dict())
    while True:

        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
