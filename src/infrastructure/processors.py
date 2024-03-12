from uuid import UUID

from src.core.interfaces.processors import UrlProcessor as IUrlProcessor
from src.infrastructure.tasks import process_url


class UrlProcessor(IUrlProcessor):
    def process(self, short_url: UUID, original_url: str) -> None:
        process_url.apply_async(args=(short_url, original_url))
