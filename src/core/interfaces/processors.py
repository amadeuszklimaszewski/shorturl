from abc import ABC, abstractmethod
from uuid import UUID

class UrlProcessor(ABC):
    @abstractmethod
    def process(self, short_url: UUID, original_url: str) -> None:
        ...
