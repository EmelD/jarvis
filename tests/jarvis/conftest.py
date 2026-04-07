import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from jarvis.core.app import create_application


@pytest.fixture(scope="session")
async def base_url() -> str:
    return "https://jarvis"


@pytest.fixture(scope="session")
async def app() -> FastAPI:
    return create_application()


@pytest.fixture
async def client(app: FastAPI, base_url: str):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=base_url
    ) as client:
        yield client
