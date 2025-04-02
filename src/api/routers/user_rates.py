import logging

from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import SessionDep, UserDep
from src.api.schemas import ApiResponse, ErrorResponse
from src.exceptions.base import AlreadyExistsError, NotFoundError
from src.schemas.user_rate import UserRateCreate, UserRateGet
from src.services.user_rate import UserRateService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/user_rates", tags=["User Rates"])


@router.get("")
async def get_user_rates(
    session: SessionDep,
    user: UserDep,
) -> ApiResponse[list[UserRateGet]]:
    user_rate_service = UserRateService(session)

    user_rates = await user_rate_service.get_all(user.id)

    return ApiResponse(data=user_rates)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {"model": ErrorResponse},
    },
)
async def create_user_rate(
    user_rate: UserRateCreate,
    session: SessionDep,
    user: UserDep,
) -> UserRateGet:
    user_rate_service = UserRateService(session)

    try:
        new_user_rate = await user_rate_service.create(user_rate, user)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=[{"msg": e.detail}]
        )
    except AlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=[{"msg": e.detail}]
        )

    return new_user_rate
