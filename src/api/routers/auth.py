from fastapi import APIRouter, HTTPException, Response, status

from src.api.dependencies import SessionDep
from src.api.schemas import ErrorResponse
from src.exceptions.auth import (
    AuthError,
)
from src.schemas.auth import Token
from src.schemas.user import UserLogin, UserRegister
from src.services.user import UserService

router = APIRouter(tags=["Auth"])


@router.post(
    "/register",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
    },
)
async def register(
    user_data: UserRegister,
    session: SessionDep,
) -> dict:
    user_service = UserService(session)
    try:
        await user_service.create_user(user_data)
    except AuthError as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            [{"msg": e.detail}],
        ) from AuthError

    return {"success": True}


@router.post(
    "/login",
    response_model=Token,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse},
    },
)
async def login(
    response: Response,
    user_in: UserLogin,
    session: SessionDep,
):
    user_service = UserService(session)
    try:
        token = await user_service.authenticate_user(user_in)
    except AuthError as e:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            [{"msg": e.detail}],
        ) from AuthError

    response.set_cookie("access_token", token.access_token, httponly=True)
    return token
