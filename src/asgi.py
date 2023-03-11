from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from db import pool
from settings import settings

from quiz.fastapi import router as titles_router


def init_routers(app: FastAPI) -> FastAPI:
    app.include_router(titles_router, tags=["titles"])
    return app


def get_app() -> FastAPI:
    app: FastAPI = FastAPI()
    init_routers(app)

    # settings.static_path.mkdir(parents=True, exist_ok=True)

    app.mount(settings.static_root, StaticFiles(directory=settings.static_path))
    return app


app = get_app()

@app.on_event("startup")
async def open_pool() -> None:
    await pool.open()

@app.on_event("shutdown")
async def close_pool()-> None:
    await pool.close()