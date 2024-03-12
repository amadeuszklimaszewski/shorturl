from abc import ABC, abstractmethod
from typing import Any


class UrlProcessor(ABC):
    @abstractmethod
    async def process(self, url_data: dict[str, Any]):
        ...
