from src.core.interfaces.processors import UrlProcessor as IUrlProcessor
from src.infrastructure.tasks import process_url


class UrlProcessor(IUrlProcessor):
    def process(self):
        process_url.apply_async(args=())
