from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncConnection

from src.core.interfaces.processors import UrlProcessor as IUrlProcessor
from src.core.interfaces.repositories import UrlRepository as IUrlRepository
from src.core.services import UrlService
from src.infrastructure.database.connection import get_db
from src.infrastructure.processors import UrlProcessor
from src.infrastructure.repositories.url import UrlRepository


def get_url_repository(
    conn: AsyncConnection = Depends(get_db),
) -> IUrlRepository:
    return UrlRepository(conn)


def get_url_processor() -> IUrlProcessor:
    return UrlProcessor()


def get_url_service(
    url_repository: IUrlRepository = Depends(get_url_repository),
    url_processor: IUrlProcessor = Depends(get_url_processor),
) -> UrlService:
    return UrlService(repository=url_repository, processor=url_processor)
