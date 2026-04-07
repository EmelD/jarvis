import pytest
from unittest.mock import patch
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check_started(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "Healthy"
    assert data[0]["name"] == "API"
    assert data[0]["description"] == "API is healthy"


@pytest.mark.asyncio
@patch("jarvis.api.health_routes.has_started", return_value=False)
async def test_health_check_not_started(mock_has_started, client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 503
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "Unhealthy"
    assert data[0]["name"] == "API"
    assert data[0]["description"] == "Application is still starting up"


@pytest.mark.asyncio
async def test_readiness_probe_started(client: AsyncClient):
    response = await client.get("/readiness")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "Healthy"
    assert data[0]["name"] == "API"
    assert data[0]["description"] == "API is healthy"


@pytest.mark.asyncio
@patch("jarvis.api.health_routes.has_started", return_value=False)
async def test_readiness_probe_not_started(mock_has_started, client: AsyncClient):
    response = await client.get("/readiness")
    assert response.status_code == 503
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "Unhealthy"
    assert data[0]["name"] == "API"
    assert data[0]["description"] == "Application is still starting up"


@pytest.mark.asyncio
async def test_liveness_probe(client: AsyncClient):
    response = await client.get("/liveness")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "Healthy"
    assert data[0]["name"] == "API"
    assert data[0]["description"] == "API is healthy"


@pytest.mark.asyncio
async def test_startup_probe_started(client: AsyncClient):
    response = await client.get("/startup")
    assert response.status_code == 200
    data = response.json()
    assert data["startup"] is True


@pytest.mark.asyncio
@patch("jarvis.api.health_routes.has_started", return_value=False)
async def test_startup_probe_not_started(mock_has_started, client: AsyncClient):
    response = await client.get("/startup")
    assert response.status_code == 503
    data = response.json()
    assert data["startup"] is False
    assert data["error"] == "Application is still starting up"
