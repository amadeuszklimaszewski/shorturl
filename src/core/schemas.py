from pydantic import BaseModel


class ShortenUrlCreateSchema(BaseModel):
    url: str
