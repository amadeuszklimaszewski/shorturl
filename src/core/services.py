import uuid

from src.core.interfaces.processors import UrlProcessor
from src.core.interfaces.repositories import UrlRepository
from src.core.models import ShortenedUrl
from src.settings import settings


class UrlService:
    def __init__(self, repository: UrlRepository, processor: UrlProcessor) -> None:
        self.repository = repository
        self.processor = processor

    def generate_short_url(self) -> uuid.UUID:
        return uuid.uuid4()

    def get_full_shortened_url(self, short_url: uuid.UUID) -> str:
        return f"http://{settings.HOST}:{settings.PORT}/{short_url}"

    async def create_shortened_url(self, url: str) -> str:
        if url_in_db := await self.repository.get_by_original_url(url):
            return self.get_full_shortened_url(url_in_db.short_url)

        short_url = self.generate_short_url()
        shortened_url = ShortenedUrl(short_url=short_url, original_url=url)
        self.processor.process(shortened_url.short_url, shortened_url.original_url)
        return self.get_full_shortened_url(shortened_url.short_url)

    async def get_original_url(self, shortened_url: uuid.UUID) -> str:
        url_in_db = await self.repository.get(pk=shortened_url)
        return url_in_db.original_url
