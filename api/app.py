import time
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from api.admin import setup_admin

from api.router.user import router as user_router


def setup_app(app: FastAPI):
    @app.middleware("http")
    async def access_log(request: Request, call_next):
        start_time = time.time()
        response: Response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        logger.info(f'[{request.client.host}] {request.method} {request.url.path} [{response.status_code}] {process_time:.3f}')
        return response

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    setup_admin(app)

    app.include_router(user_router, prefix='/api/v1')
    # app.include_router(log_group_router, prefix='/api/v1')
    # app.include_router(log_level_router, prefix='/api/v1')
    # app.include_router(log_item_router, prefix='/api/v1')


app = FastAPI(
    title='SportsMap API',
    version='2.0'
)

setup_app(app)

__all__ = [
    app
]
