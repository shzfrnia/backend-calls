from fastapi import APIRouter

from app.errors import (
    RequestConflictError,
    BadRequestError,
    AccessDeniedError
)

from app import crud

from app.api.deps import CurrentUser, SessionDep

from app.core.security import get_password_hash, verify_password

from app.models.message import Message
from app.models.password import UpdatePassword
from app.models.user import UserPublic, UserUpdateMe


router = APIRouter(prefix="/users", tags=["users"])


@router.patch("/me", response_model=UserPublic)
def update_current_user(
    *, session: SessionDep, user_in: UserUpdateMe, current_user: CurrentUser
) -> UserPublic:
    """
    Update own user.
    """

    if user_in.email:
        existing_user = crud.get_user_by_username(
            session=session, username=user_in.email
        )

        if existing_user and existing_user.id != current_user.id:
            raise RequestConflictError("User with this email already exists")

    user_data = user_in.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user


@router.patch("/me/password", response_model=Message)
def update_password(
    *, session: SessionDep, body: UpdatePassword, current_user: CurrentUser
) -> Message:
    """
    Update own password.
    """
    verified, _ = verify_password(
        body.current_password, current_user.hashed_password
    )

    if not verified:
        raise BadRequestError("Incorrect password")

    if body.current_password == body.new_password:
        raise BadRequestError(
            "New password cannot be the same as the current one"
        )

    hashed_password = get_password_hash(body.new_password)
    current_user.hashed_password = hashed_password
    session.add(current_user)
    session.commit()

    return Message(message="Password updated successfully")


@router.get("/me", response_model=UserPublic)
def get_current_user(current_user: CurrentUser) -> UserPublic:
    """
    Get current user.
    """
    return current_user


@router.delete("/me", response_model=Message)
def delete_current_user(session: SessionDep, current_user: CurrentUser) -> Message:
    """
    Delete own user.
    """
    if current_user.is_superuser:
        raise AccessDeniedError(
            "Super users are not allowed to delete themselves"
        )

    session.delete(current_user)
    session.commit()

    return Message(message="User deleted successfully")
