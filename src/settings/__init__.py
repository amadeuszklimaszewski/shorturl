from pydantic_settings import SettingsConfigDict

from src.settings.application import AppSettings
from src.settings.celery import CelerySettings
from src.settings.database import DatabaseSettings


class Settings(
    AppSettings,
    CelerySettings,
    DatabaseSettings,
):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
