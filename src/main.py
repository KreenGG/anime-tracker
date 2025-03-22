from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.api import router as api_router
from src.logger import setup_logging
from src.pages import router as pages_router


def setup_templates(app: FastAPI) -> None:
    base_dir = Path(__file__).parent.parent
    static_dir = base_dir / "static"

    app.mount("/static", StaticFiles(directory=static_dir), "static")

    @app.get("/favicon.ico", include_in_schema=False)
    async def get_favicon():
        favicon_path = static_dir / "favicon.ico"
        return FileResponse(favicon_path)

    app.include_router(pages_router)


def create_app():
    setup_logging()

    app = FastAPI(
        title="Anime Tracker",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
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

    app.include_router(api_router)
    setup_templates(app)

    return app
