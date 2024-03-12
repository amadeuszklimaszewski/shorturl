import uuid

import pytest
import pytest_asyncio

from src.core.exceptions import DoesNotExistError
from src.core.models import ShortenedUrl
from src.core.services import UrlService
from src.settings import settings
from tests.fakes import UrlRepository


@pytest_asyncio.fixture
async def shortened_url_in_db(url_repository: UrlRepository) -> ShortenedUrl:
    original_url = "https://example.com"
    short_url = uuid.uuid4()
    model = ShortenedUrl(short_url=short_url, original_url=original_url)
    await url_repository.persist(model)
    return model


@pytest.mark.asyncio
async def test_generate_short_url(url_service: UrlService):
    url = url_service.generate_short_url()

    assert isinstance(url, uuid.UUID)


@pytest.mark.asyncio
async def test_get_full_shortened_url(url_service: UrlService):
    short_url = uuid.uuid4()
    url = url_service.get_full_shortened_url(short_url)

    assert url == f"http://{settings.HOST}:{settings.PORT}/{short_url}"


@pytest.mark.asyncio
async def test_get_original_url(
    url_service: UrlService, shortened_url_in_db: ShortenedUrl
):
    result = await url_service.get_original_url(shortened_url_in_db.short_url)

    assert result == shortened_url_in_db.original_url


@pytest.mark.asyncio
async def test_get_original_url_does_not_exist(url_service: UrlService):
    short_url = uuid.uuid4()
    with pytest.raises(DoesNotExistError):
        await url_service.get_original_url(short_url)


@pytest.mark.asyncio
async def test_create_shortened_url_existing_url(
    url_service: UrlService, shortened_url_in_db: ShortenedUrl
):
    result = await url_service.create_shortened_url(shortened_url_in_db.original_url)

    assert (
        result
        == f"http://{settings.HOST}:{settings.PORT}/{shortened_url_in_db.short_url}"
    )


@pytest.mark.asyncio
async def test_create_shortened_url_new_url(url_service: UrlService):
    new_url = "https://example.com"

    result = await url_service.create_shortened_url(new_url)

    assert isinstance(result, str)
    short_url = uuid.UUID(
        result.replace(f"http://{settings.HOST}:{settings.PORT}/", "")
    )
    url_in_db = await url_service.get_original_url(short_url)
    assert url_in_db == new_url
