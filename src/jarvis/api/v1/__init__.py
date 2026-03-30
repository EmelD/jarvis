from fastapi import APIRouter
from fastapi.responses import JSONResponse

from jarvis.api.schemas import ErrorResponse


router = APIRouter(
    prefix="/v1",
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
