from fastapi import APIRouter

from app.core.config import settings

from app.api.routes import (
    login,
    users,
    servers,
    invites,
    roles,
    utils,

    ws,

    private
)


api_router = APIRouter()

api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(servers.router)
api_router.include_router(invites.router)
api_router.include_router(roles.router)
api_router.include_router(utils.router)

api_router.include_router(ws.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
