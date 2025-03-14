from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import SessionDep
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
        status.HTTP_200_OK: {
            "description": "Succesful user registration",
        },
        status.HTTP_400_BAD_REQUEST: {},
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
            e.detail,
        ) from AuthError

    return {"success": True}


@router.post("/login", response_model=Token)
async def login(
    user_in: UserLogin,
    session: SessionDep,
):
    user_service = UserService(session)
    try:
        token = await user_service.authenticate_user(user_in)
    except AuthError as e:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            e.detail,
        ) from AuthError

    return token
