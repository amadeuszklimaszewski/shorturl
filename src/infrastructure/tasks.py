from src.infrastructure.celery import app
from src.infrastructure.database.connection import engine
from asgiref.sync import async_to_sync
from src.infrastructure.repositories.url import UrlRepository
from uuid import UUID
from src.core.models import ShortenedUrl

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
    
    async_to_sync(_persist)(shortened_url)
