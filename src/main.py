from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api import router as api_router
from src.logger import setup_logging
from src.pages import router as pages_router


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

    # frontend pages
    app.mount("/static", StaticFiles(directory="src/static"), "static")
    app.include_router(pages_router)

    return app
