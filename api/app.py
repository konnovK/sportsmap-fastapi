import os
import time

import starlette.exceptions
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.exceptions import ValidationException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from starlette.responses import JSONResponse

from api.admin import setup_admin

from api.router.user import router as user_router
from api.router.facility import router as facility_router


def create_app() -> FastAPI:
    app = FastAPI(
        title='SportsMap API',
        version='2.0'
    )

    @app.middleware("http")
    async def access_log(request: Request, call_next):
        start_time = time.time()
        response: Response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        logger.info(
            f'[{request.client.host}] [{os.getpid()}] '
            f'{request.method} {request.url.path} '
            f'[{response.status_code}] {process_time:.3f}'
        )
        return response

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    def exception_handler(request: Request, exception: Exception):
        if isinstance(exception, ValidationException):
            exception: ValidationException
            return JSONResponse(content=exception.errors(),status_code=422)
        elif isinstance(exception, starlette.exceptions.HTTPException):
            exception: HTTPException
            exception_body = exception.detail
            exception_status = exception.status_code
            if isinstance(exception_body, dict):
                return JSONResponse(content=exception_body, status_code=exception_status)
            else:
                return Response(content=exception_body, status_code=exception_status)
        else:
            logger.debug(type(exception))
            logger.error(exception)
            return JSONResponse(content={}, status_code=500)
    for i in range(400, 600):
        app.add_exception_handler(i, exception_handler)

    setup_admin(app)

    ROUTE_PREFIX = '/v1'

    app.include_router(user_router, prefix=ROUTE_PREFIX)
    app.include_router(facility_router, prefix=ROUTE_PREFIX)

    return app


app = create_app()

__all__ = [
    app
]
