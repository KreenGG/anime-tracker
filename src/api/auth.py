from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.exceptions.auth import (
    AuthError,
)
from src.schemas.auth import Token
from src.schemas.user import UserLogin, UserRegister
from src.services.user import authenticate_user, create_user

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
    except AuthError as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            e.detail,
        ) from AuthError

    return {"success": True}

@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user_data = UserLogin(
        email=form_data.username,
        password=form_data.password,
    )
    try:
        token = await authenticate_user(user_data)
    except AuthError as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            e.detail,
        ) from AuthError


    return {
        "access_token": token,
        "token_type": "bearer",
    }
