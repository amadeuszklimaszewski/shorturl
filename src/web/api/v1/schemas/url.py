from pydantic import BaseModel, HttpUrl


class ShortenUrlInputSchema(BaseModel):
    url: HttpUrl


class ShortenedUrlOutputSchema(BaseModel):
    url: HttpUrl
