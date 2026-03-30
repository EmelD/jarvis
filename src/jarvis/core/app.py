import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from jarvis.api.routes import api_router
from jarvis.core.lifespan import started, starting, stopped, stopping
from jarvis.core.exceptions import register_exception_handler
from jarvis.core.settings import app_settings

logger = logging.getLogger(__name__)


def create_application() -> FastAPI:
    starting()

    @asynccontextmanager
    async def app_state_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        started()

        yield

        stopping()
        stopped()

    app = FastAPI(
        root_path="",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        title="Jarvis",
        lifespan=app_state_lifespan,
        version=app_settings.VERSION,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    register_exception_handler(app)

    return app
