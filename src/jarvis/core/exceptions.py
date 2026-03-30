from fastapi import status
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from logging import getLogger

logger = getLogger(__name__)


class BaseException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

    @property
    def content(self) -> dict:
        return {
            "detail": self.message,
            "status": self.status_code,
        }


class InternalServerErrorException(BaseException):
    def __init__(self, message: str = "Internal server error"):
        super().__init__(message=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GatewayTimeoutException(BaseException):
    def __init__(self, message: str = "Gateway timeout"):
        super().__init__(message=message, status_code=status.HTTP_504_GATEWAY_TIMEOUT)


class ClientSideException(BaseException):
    def __init__(self, message: str = "Bad request"):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)


class UnauthorizedException(ClientSideException):
    def __init__(self, message: str):
        super().__init__(message=message)
        self.status_code = status.HTTP_401_UNAUTHORIZED


class ForbiddenException(ClientSideException):
    def __init__(self, message: str):
        super().__init__(message=message)
        self.status_code = status.HTTP_403_FORBIDDEN


class NotFoundException(ClientSideException):
    def __init__(self, message: str):
        super().__init__(message=message)
        self.status_code = status.HTTP_404_NOT_FOUND


class PreconditionFailedException(ClientSideException):
    def __init__(self, message: str):
        super().__init__(message=message)
        self.status_code = status.HTTP_412_PRECONDITION_FAILED


class UnProcessableEntityException(ClientSideException):
    def __init__(self, message: str):
        super().__init__(message=message)
        self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


def register_exception_handler(app: FastAPI):

    @app.exception_handler(BaseException)
    async def exception_handler(_request: Request, exc: BaseException):
        if (
            status.HTTP_400_BAD_REQUEST <= exc.status_code <= status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED
        ):
            return JSONResponse(status_code=exc.status_code, content=exc.content)
        else:
            logger.exception(msg="Exception occurred", exc_info=exc)
            return JSONResponse(status_code=exc.status_code, content=exc.content)
