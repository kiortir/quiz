from pydantic import BaseSettings
from pathlib import Path
import dotenv
import os

env = dotenv.load_dotenv()
API_TOKEN = os.environ.get("API_TOKEN")


class Settings(BaseSettings):

    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"

    static_root: str = "/static/"
    static_path: Path = Path("./static")

    host: str = "https://stream.kiortir.ru"
    API_TOKEN: str

    ssl_cert: str = "/home/kiortir/projects/quiz/cert/server.crt"
    ssl_key: str = "/home/kiortir/projects/quiz/cert/server.key"


settings = Settings()
