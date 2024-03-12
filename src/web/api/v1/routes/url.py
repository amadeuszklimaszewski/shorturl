from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from src.web.api.v1.annotations import UrlService
from src.web.api.v1.schemas.url import ShortenedUrlOutputSchema, ShortenUrlInputSchema

url_router = APIRouter()


@url_router.post(
    "/shorten/",
    status_code=status.HTTP_201_CREATED,
    response_model=ShortenedUrlOutputSchema,
)
async def shorten(
    url: ShortenUrlInputSchema,
    service: UrlService,
):
    new_url = await service.create_shortened_url(str(url.url))
    return {"url": new_url}


@url_router.get(
    "/{short_url}/",
    status_code=status.HTTP_302_FOUND,
)
async def redirect_to_original_url(
    short_url: str,
    service: UrlService,
):
    original_url = await service.get_original_url(short_url)
    return RedirectResponse(url=original_url)
