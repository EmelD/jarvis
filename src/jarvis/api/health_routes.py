from logging import getLogger

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from jarvis.core.lifespan import has_started

DESCRIPTION_API_IS_HEALTHY = "API is healthy"
DESCRIPTION_APP_STARTING = "Application is still starting up"
DESCRIPTION_APP_READY = "Application is ready"

logger = getLogger(__name__)

health_router = APIRouter(
    default_response_class=JSONResponse,
)


@health_router.get("/health")
async def health_check() -> JSONResponse:
    if not has_started():
        return JSONResponse(
            content=[{
                "status": "Unhealthy",
                "name": "API",
                "description": DESCRIPTION_APP_STARTING,
            }],
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    return JSONResponse(
        content=[{
            "status": "Healthy",
            "name": "API",
            "description": DESCRIPTION_API_IS_HEALTHY
        }],
        status_code=status.HTTP_200_OK,
    )


@health_router.get("/readiness")
async def readiness_probe() -> JSONResponse:
    if not has_started():
        return JSONResponse(
            content=[{
                "status": "Unhealthy",
                "name": "API",
                "description": DESCRIPTION_APP_STARTING,
            }],
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    return JSONResponse(
        content=[{
            "status": "Healthy",
            "name": "API",
            "description": DESCRIPTION_API_IS_HEALTHY,
        }],
        status_code=status.HTTP_200_OK,
    )


@health_router.get("/liveness")
async def liveness_probe() -> JSONResponse:
    return JSONResponse(
        content=[{
            "status": "Healthy",
            "name": "API",
            "description": DESCRIPTION_API_IS_HEALTHY,
        }],
        status_code=status.HTTP_200_OK,
    )


@health_router.get("/startup")
async def startup_probe() -> JSONResponse:
    if has_started():
        return JSONResponse(
            content={"startup": True},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"startup": False, "error": DESCRIPTION_APP_STARTING},
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    )
