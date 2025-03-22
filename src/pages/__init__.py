from fastapi import APIRouter

from .routers import router as pages_router

router = APIRouter(
    prefix="",
    include_in_schema=False,
)

router.include_router(pages_router)
