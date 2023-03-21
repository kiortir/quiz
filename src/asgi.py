from uuid import UUID

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import telebot
from bot import bot
from db import pool
from quiz.fastapi import router as titles_router
from settings import settings


def init_routers(app: FastAPI) -> FastAPI:
    app.include_router(titles_router, tags=["titles"])
    return app


def get_app() -> FastAPI:
    app: FastAPI = FastAPI()
    init_routers(app)
    app.mount(settings.static_root, StaticFiles(directory=settings.static_path))
    return app


app = get_app()


@app.post(f"/webhook/{settings.API_TOKEN}/")
def process_webhook(update: dict):
    """
    Process webhook calls
    """
    if update:
        update = telebot.types.Update.de_json(update)
        bot.process_new_updates([update])
    else:
        return


@app.on_event("startup")
async def open_pool() -> None:
    await pool.open()
    # await bot.remove_webhook()
    # await bot.set_webhook(url=settings.host)
    # bot


@app.on_event("shutdown")
async def close_pool() -> None:
    await pool.close()
