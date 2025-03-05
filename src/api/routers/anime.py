import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import NotFoundError
from src.api.schemas import ApiResponse, ErrorResponse
from src.database import get_session
from src.schemas.anime import Anime
from src.services.anime import AnimeService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/anime",
    tags=["Anime"],
)

@router.get(
    "",
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[list[Anime]]},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
    },
)
async def get_animes(
    session: Annotated[AsyncSession, Depends(get_session)],
    offset:  Annotated[int | None, Query(ge=0)] = None,
    limit: Annotated[int | None, Query(ge=0)] = None,
):
    anime_service = AnimeService()
    anime_list = await anime_service.get_all(session, offset, limit)

    if not anime_list:
        logger.debug("Animes not found (offset=%d, limit=%d)", offset, limit)
        raise NotFoundError

    return ApiResponse(data=anime_list)

@router.get(
    "/{id}",
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[Anime]},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
    },
)
async def get_single_anime(
    session: Annotated[AsyncSession, Depends(get_session)],
    id: int,
):
    anime_service = AnimeService()
    anime = await anime_service.get_single(session, id)

    if not anime:
        logger.debug("Anime not found (id=%d)", id)
        raise NotFoundError

    return ApiResponse(data=anime)
