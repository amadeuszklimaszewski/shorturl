from fastapi import FastAPI

from src.web.api.v1.router import api_router


def get_app() -> FastAPI:
    app = FastAPI(
        title="shorturl",
        version="1.0.0",
        docs_url="/api/docs",
    )
    app.include_router(router=api_router, prefix="/api")
    return app
