from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import router
from src.api.dependencies import get_current_user
from src.logger import setup_logging
from src.schemas.user import User

setup_logging()

app = FastAPI(
    title="Anime Tracker",
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/test_with_auth")
async def test_auth(
    user: Annotated[User, Depends(get_current_user)],
):
    return user


@app.get("/test_without_auth")
async def test_without_auth():
    return "Free endpoint"
