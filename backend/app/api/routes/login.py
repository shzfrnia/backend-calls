from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.errors import BadRequestError

from app.core import security

from app.api.deps import SessionDep

from app.core.config import settings

from app.models.token import Token
from app.models.user import UserPublic, UserCreate, UserRegister

from app.crud import user as user_crud


router = APIRouter(tags=["login"])


@router.post("/signup", response_model=UserPublic)
def signup(session: SessionDep, user_in: UserRegister) -> UserPublic:
    """
    Create new user without the need to be logged in.
    """
    user = user_crud.get_user_by_email_or_login(
        session=session, email=user_in.email, login=user_in.login
    )

    if user:
        raise BadRequestError(
            "The user with this email or login already exists in the system"
        )

    user = user_crud.create_user(
        session=session, user_create=UserCreate.model_validate(user_in)
    )

    return user


@router.post("/signin")
def signin(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = user_crud.authenticate(
        session=session, username=form_data.username, password=form_data.password
    )

    if not user:
        raise BadRequestError("Incorrect username or password")
    elif not user.is_active:
        raise BadRequestError("Inactive user")

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )
