from typing import Any, AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine

from src.core.interfaces.processors import UrlProcessor as IUrlProcessor
from src.core.interfaces.repositories import UrlRepository as IUrlRepository
from src.core.services import UrlService
from src.infrastructure.database.metadata import metadata
from src.infrastructure.database.tables import load_all_tables
from src.settings import Settings
from src.web.api.v1.dependencies import get_url_processor, get_url_repository
from src.web.application import get_app
from tests.fakes import InMemoryDB, UrlProcessor, UrlRepository


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest_asyncio.fixture
async def async_db_engine() -> AsyncGenerator[AsyncEngine, None]:
    load_all_tables()

    settings = Settings(TESTING=True)  # type: ignore
    engine = create_async_engine(settings.postgres_url)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)

    try:
        yield engine
    finally:
        await engine.dispose()

    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest_asyncio.fixture
async def async_db_connection(
    async_db_engine: AsyncEngine,
) -> AsyncGenerator[AsyncConnection, None]:
    async with async_db_engine.begin() as conn:
        yield conn
        await conn.rollback()


@pytest.fixture
def in_memory_db() -> InMemoryDB:
    return InMemoryDB()


@pytest.fixture
def url_repository(in_memory_db: InMemoryDB):
    repository = UrlRepository()
    repository.set_db(in_memory_db)
    return repository


@pytest.fixture
def url_processor(in_memory_db: InMemoryDB):
    processor = UrlProcessor()
    processor.set_db(in_memory_db)
    return processor


@pytest.fixture
def url_service(
    url_repository: IUrlRepository, url_processor: IUrlProcessor
) -> UrlService:
    return UrlService(repository=url_repository, processor=url_processor)


@pytest.fixture
def fastapi_app(
    url_repository: IUrlRepository,
    url_processor: IUrlProcessor,
) -> FastAPI:
    app = get_app()
    app.dependency_overrides[get_url_processor] = lambda: url_processor
    app.dependency_overrides[get_url_repository] = lambda: url_repository
    return app


@pytest_asyncio.fixture
async def client(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(
        transport=transport, base_url="http://test/api/v1"
    ) as client:
        yield client
