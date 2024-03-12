from abc import ABC, abstractmethod
from typing import Type
from uuid import UUID

from pydantic import BaseModel

from src.core.models import ShortenedUrl


class BaseRepository[PK, Model: BaseModel](ABC):
    @abstractmethod
    def get(self, pk: PK) -> Model:
        ...

    @abstractmethod
    def persist(self, model: Model) -> None:
        ...

    @abstractmethod
    def delete(self, pk: PK) -> None:
        ...

    @property
    @abstractmethod
    def _model(self) -> Type[Model]:
        ...


class UrlRepository(BaseRepository[UUID, ShortenedUrl], ABC):
    ...
