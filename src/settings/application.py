from pathlib import Path

from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    ENVIRONMENT: str = "DEV"

    HOST: str = "127.0.0.1"
    PORT: int = 8000
    WORKERS_COUNT: int = 1
    RELOAD: bool = False
