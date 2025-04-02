import logging

from fastapi import APIRouter

from src.api.dependencies import SessionDep, UserDep
from src.schemas.user import UserGet, UserUpdate
from src.services.user import UserService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/whoami",
    description="Show current user info",
    response_model=UserGet,
)
async def get_current_user(
    session: SessionDep,
    user: UserDep,
):
    user_service = UserService(session)
    user = await user_service.get_user_by_id(user.id)

    return user


@router.patch(
    "",
    description="Update user",
)
async def update_user(
    session: SessionDep,
    user: UserDep,
    updated_user_data: UserUpdate,
) -> UserGet:
    user_service = UserService(session)

    changed_user = await user_service.update_user(
        user.id,
        updated_user_data,
    )
    return changed_user
