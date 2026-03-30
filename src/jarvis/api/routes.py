from fastapi import APIRouter
from fastapi.responses import JSONResponse

from jarvis.api.health_routes import health_router
from jarvis.api.schemas import ErrorResponse
from jarvis.api.v1 import router as v1_router


api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
api_router.include_router(health_router)
api_router.include_router(v1_router)
