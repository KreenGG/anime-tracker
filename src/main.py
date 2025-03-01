from typing import Annotated

from fastapi import Depends, FastAPI

from src.api import router
from src.api.dependencies import get_current_user
from src.schemas.user import UserDTO

app = FastAPI()

app.include_router(router)

@app.get("/test")
async def test_auth(
    user: Annotated[UserDTO, Depends(get_current_user)],
):
    return user
