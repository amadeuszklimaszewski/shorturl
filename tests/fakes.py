from uuid import UUID

from src.core.exceptions import AlreadyExistsError, DoesNotExistError
from src.core.interfaces.processors import UrlProcessor as IUrlProcessor
from src.core.interfaces.repositories import UrlRepository as IUrlRepository
from src.core.models import ShortenedUrl


class InMemoryDB:
    def __init__(self) -> None:
        self.urls: dict[UUID, ShortenedUrl] = {}


class UrlRepository(IUrlRepository):
    _db: InMemoryDB

    def set_db(self, db: InMemoryDB) -> None:
        self._db = db

    async def get(self, pk: UUID) -> ShortenedUrl:
        try:
            return self._db.urls[pk]
        except KeyError:
            raise DoesNotExistError(
                f"{self.__class__.__name__} could not find {ShortenedUrl.__name__} with given PK - {pk}",
            )

    async def get_by_original_url(self, url: str) -> ShortenedUrl | None:
        for url_in_db in self._db.urls.values():
            if url_in_db.original_url == url:
                return url_in_db
        
        return None

    async def persist(self, model: ShortenedUrl) -> None:
        if model.short_url in self._db.urls:
            raise AlreadyExistsError(
                f"{self.__class__.__name__} could not persist {model}: record with given PK already exists",
            )
        self._db.urls[model.short_url] = model


class UrlProcessor(IUrlProcessor):
    _db: InMemoryDB

    def set_db(self, db: InMemoryDB) -> None:
        self._db = db

    def process(self, short_url: UUID, original_url: str) -> None:
        self._db.urls[short_url] = ShortenedUrl(
            short_url=short_url, original_url=original_url
        )
