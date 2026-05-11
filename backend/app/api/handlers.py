from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.errors import (
    ObjectNotFoundError,
    AccessDeniedError,
    BadRequestError,
    RequestConflictError
)


def setup_handlers(app: FastAPI):
    @app.exception_handler(ObjectNotFoundError)
    async def not_found_handler(request: Request, exc: ObjectNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(AccessDeniedError)
    async def access_denied_handler(request: Request, exc: AccessDeniedError):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": str(exc)},
        )

    @app.exception_handler(BadRequestError)
    async def bad_request_handler(request: Request, exc: BadRequestError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )

    @app.exception_handler(RequestConflictError)
    async def request_conflict_handler(request: Request, exc: RequestConflictError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc)},
        )
