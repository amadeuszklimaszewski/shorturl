import asyncio
from uuid import UUID

from src.core.models import ShortenedUrl
from src.infrastructure.celery import app
from src.infrastructure.database.connection import engine
from src.infrastructure.repositories.url import UrlRepository


@app.task(
    ignore_result=True,
    autoretry_for=(Exception,),
    acks_late=True,
)
def process_url(short_url: UUID, original_url: str):
    shortened_url = ShortenedUrl(short_url=short_url, original_url=original_url)

    async def _persist(model: ShortenedUrl):
        async with engine.begin() as conn:
            repository = UrlRepository(conn)
            await repository.persist(model)

    asyncio.run(_persist(shortened_url))
