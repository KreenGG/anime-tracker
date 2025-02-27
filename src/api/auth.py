from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.exceptions.user import (
    UserError,
)
from src.schemas.user import UserLogin, UserRegister
from src.services.user import create_user, login_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter(tags=["Auth"])

@router.post(
    "/register",
    responses={
        status.HTTP_200_OK: {
            "description": "Succesful user registration",
        },
        status.HTTP_400_BAD_REQUEST:{
        },
    },
)
async def register(user_data: UserRegister) -> dict:
    try:
        await create_user(user_data)
    except UserError as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            e.detail,
        ) from UserError

    return {"success": True}

@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user_data = UserLogin(
        email=form_data.username,
        password=form_data.password,
    )
    try:
        token = await login_user(user_data)
    except UserError as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            e.detail,
        ) from UserError


    return {"access_token": token}


# TODO: Сделать функцию получения пользователя и проверки токена, для остального функционала
@router.get("/check")
async def check_token(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    return {"token": token}
