from fastapi import APIRouter

from .anime import router as animes_router
from .auth import router as auth_router
from .user import router as users_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(animes_router)
router.include_router(users_router)
