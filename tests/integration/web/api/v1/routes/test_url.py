from uuid import UUID, uuid4

import pytest
from fastapi import status
from httpx import AsyncClient, Response

from src.settings import settings


@pytest.mark.asyncio
async def test_shorten_url(
    client: AsyncClient,
):
    data = {"url": "https://example.com"}
    response: Response = await client.post("/shorten/", json=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert "url" in response.json()
    assert isinstance(response.json()["url"], str)


@pytest.mark.asyncio
async def test_redirect_to_original_url(
    client: AsyncClient,
):
    full_url: str = (
        await client.post("/shorten/", json={"url": "https://example.com"})
    ).json()["url"]
    short_url = full_url.replace(f"http://{settings.HOST}:{settings.PORT}/", "")

    response: Response = await client.get(f"/{short_url}/")

    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.is_redirect is True


@pytest.mark.asyncio
async def test_redirect_to_original_url_invalid_url(
    client: AsyncClient,
):
    response: Response = await client.get(f"/{uuid4()}/")

    assert response.status_code == status.HTTP_404_NOT_FOUND
