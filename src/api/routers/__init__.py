from fastapi import APIRouter

from .anime import router as anime_router
from .auth import router as auth_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(anime_router)
