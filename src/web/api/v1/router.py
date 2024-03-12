from fastapi.routing import APIRouter

from src.web.api.v1.routes.url import url_router

api_router = APIRouter(tags=["v1"])
api_router.include_router(url_router)
