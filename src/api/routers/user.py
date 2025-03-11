import logging

from fastapi import APIRouter, status

from src.api.dependencies import SessionDep, UserDep
from src.api.schemas import ErrorResponse
from src.schemas.user import UserGet
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
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse},
    },
)
async def get_current_user(
    session: SessionDep,
    user: UserDep,
):
    user_service = UserService(session)
    user = await user_service.get_user_by_id(user.id)

    return user
