from pydantic import BaseSettings
from pathlib import Path


class Settings(BaseSettings):

    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    
    static_root: str = "/static/"
    static_path: Path = Path("./static")


settings = Settings()
