from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from src.api.schemas import ErrorResponse

from .anime import router as animes_router
from .auth import router as auth_router
from .user import router as users_router
from .user_rates import router as user_rates_router

router = APIRouter(
    default_response_class=ORJSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)

router.include_router(auth_router)
router.include_router(animes_router)
router.include_router(users_router)
router.include_router(user_rates_router)
