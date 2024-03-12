from typing import Annotated

from fastapi import Depends

from src.core.services import UrlService as _UrlService
from src.web.api.v1.dependencies import get_url_service

UrlService = Annotated[_UrlService, Depends(get_url_service)]
