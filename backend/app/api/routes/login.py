from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from app import crud

from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser

from app.core import security

from app.core.config import settings

from app.models.message import Message
from app.models.password import NewPassword
from app.models.token import Token
from app.models.user import UserPublic, UserUpdate, UserCreate, UserRegister

from app.utils.mail import (
    generate_password_reset_token,
    generate_reset_password_email,
    send_email,
    verify_password_reset_token,
)

router = APIRouter(tags=["login"])


@router.post("/signup", response_model=UserPublic)
def signup(session: SessionDep, user_in: UserRegister) -> UserPublic:
    """
    Create new user without the need to be logged in.
    """
    user = crud.get_user_by_email_or_login(
        session=session, email=user_in.email, login=user_in.login
    )

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email or login already exists in the system",
        )

    user = crud.create_user(
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
    user = crud.authenticate(
        session=session, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )


# @router.post("/password-recovery/{email}")
# def recover_password(email: str, session: SessionDep) -> Message:
#     """
#     Password Recovery
#     """
#     user = crud.get_user_by_email(session=session, email=email)

#     # Always return the same response to prevent email enumeration attacks
#     # Only send email if user actually exists
#     if user:
#         password_reset_token = generate_password_reset_token(email=email)
#         email_data = generate_reset_password_email(
#             email_to=user.email, email=email, token=password_reset_token
#         )
#         send_email(
#             email_to=user.email,
#             subject=email_data.subject,
#             html_content=email_data.html_content,
#         )
#     return Message(
#         message="If that email is registered, we sent a password recovery link"
#     )


# @router.post("/reset-password/")
# def reset_password(session: SessionDep, body: NewPassword) -> Message:
#     """
#     Reset password
#     """
#     email = verify_password_reset_token(token=body.token)
#     if not email:
#         raise HTTPException(status_code=400, detail="Invalid token")
#     user = crud.get_user_by_email(session=session, email=email)
#     if not user:
#         # Don't reveal that the user doesn't exist - use same error as invalid token
#         raise HTTPException(status_code=400, detail="Invalid token")
#     elif not user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     user_in_update = UserUpdate(password=body.new_password)
#     crud.update_user(
#         session=session,
#         db_user=user,
#         user_in=user_in_update,
#     )
#     return Message(message="Password updated successfully")


# @router.post(
#     "/password-recovery-html-content/{email}",
#     dependencies=[Depends(get_current_active_superuser)],
#     response_class=HTMLResponse,
# )
# def recover_password_html_content(email: str, session: SessionDep) -> Any:
#     """
#     HTML Content for Password Recovery
#     """
#     user = crud.get_user_by_email(session=session, email=email)

#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this username does not exist in the system.",
#         )
#     password_reset_token = generate_password_reset_token(email=email)
#     email_data = generate_reset_password_email(
#         email_to=user.email, email=email, token=password_reset_token
#     )

#     return HTMLResponse(
#         content=email_data.html_content, headers={
#             "subject:": email_data.subject}
#     )
