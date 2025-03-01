from typing import Annotated

from fastapi import Depends, FastAPI

from src.api import router
from src.api.dependencies import get_current_user
from src.logger import setup_logging
from src.schemas.user import UserDTO

setup_logging()

app = FastAPI()

app.include_router(router)

@app.get("/test_with_auth")
async def test_auth(
    user: Annotated[UserDTO, Depends(get_current_user)],
):
    return user

@app.get("/test_without_auth")
async def test_without_auth(
):
    return "Free endpoint"
