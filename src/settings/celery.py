from pydantic_settings import BaseSettings


class CelerySettings(BaseSettings):
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    CELERY_ACCEPT_CONTENT: list[str] = [
        "application/json",
        "application/x-python-serialize",
    ]
