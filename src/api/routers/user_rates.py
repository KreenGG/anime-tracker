import logging

from fastapi import APIRouter

from src.api.dependencies import SessionDep, UserDep
from src.api.exceptions import UnauthorizedError
from src.api.schemas import ApiResponse
from src.schemas.user_rate import UserRateCreate, UserRateGet

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/user_rates", tags=["User Rates"])


@router.post("")
async def create_user_rate(
    user_rate: UserRateCreate,
    session: SessionDep,
    user: UserDep,
) -> UserRateGet:
    if user.id != user_rate.user_id:
        logger.debug("Failed creating user rate (%d != %d)", user.id, user_rate.user_id)
        raise UnauthorizedError

    # user_rate_service = UserRateService()

    # new_user_rate = user_rate_service.create()

    return ApiResponse(data="")
