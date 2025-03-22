from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from src.api.routers.anime import get_animes, get_single_anime

router = APIRouter()

templates = Jinja2Templates(directory="src/templates")


@router.get("/")
async def get_index_html(request: Request, animes=Depends(get_animes)):
    return templates.TemplateResponse(
        name="index.html.jinja",
        context={"request": request, "animes": animes},
    )


@router.get("/animes/{id}")
async def get_anime_html(request: Request, anime=Depends(get_single_anime)):
    return templates.TemplateResponse(
        name="anime.html.jinja",
        context={"request": request, "anime": anime},
    )
