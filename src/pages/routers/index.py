from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.templating import Jinja2Templates

from src.api.routers.anime import get_animes

router = APIRouter()

templates = Jinja2Templates(directory="src/templates")


@router.get("/")
async def get_index_html(
    request: Request, response: Response, animes=Depends(get_animes)
):
    try:
        animes.data
    except HTTPException:
        print("fjsdfjsd")
    return templates.TemplateResponse(
        name="index.html.jinja",
        context={"request": request, "animes": animes},
    )
