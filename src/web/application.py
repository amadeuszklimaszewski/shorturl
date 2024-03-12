from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.core.exceptions import ApplicationError, DoesNotExistError
from src.web.api.v1.router import api_router


def get_app() -> FastAPI:
    app = FastAPI(
        title="shorturl",
        version="1.0.0",
        docs_url="/docs",
    )

    @app.exception_handler(ApplicationError)
    async def application_error_handler(
        request: Request,
        exc: ApplicationError,
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )

    @app.exception_handler(DoesNotExistError)
    async def does_not_exist_exception_handler(
        request: Request,
        exc: DoesNotExistError,
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Not found"},
        )

    app.include_router(router=api_router, prefix="")
    return app
