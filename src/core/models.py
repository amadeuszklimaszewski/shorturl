from uuid import UUID

from pydantic import BaseModel


class ShortenedUrl(BaseModel):
    short_url: UUID
    original_url: str
