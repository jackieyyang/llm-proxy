from http import HTTPStatus

import httpx
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import HTTPException, RequestValidationError
from ..util import logger_util


async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom handler for 400/500 HTTPException.

    Args:
        request: Request
        exc: HTTPException

    Returns:
        JSONResponse
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "msg": exc.detail,
            "path": request.url.path,
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom handler for 422 RequestValidationError.

    Args:
        request: Request
        exc: RequestValidationError

    Returns:
        JSONResponse
    """
    return JSONResponse(
        status_code=422,
        content={
            "code": 422,
            "msg": "参数校验失败",
            "errors": exc.errors(),
        },
    )


async def httpx_timeout_exception_handler(request: Request, exc: httpx.TimeoutException):
    """
    Handler for httpx.TimeoutException.

    Args:
        request: Request
        exc: httpx.TimeoutException

    Returns:
        JSONResponse
    """
    code = HTTPStatus.GATEWAY_TIMEOUT.value
    msg = HTTPStatus.GATEWAY_TIMEOUT.description
    detail = str(exc)

    if isinstance(exc, httpx.ConnectTimeout | httpx.ReadTimeout | httpx.WriteTimeout):
        logger_util.full_info("UPSTREAM", "HTTPX Timeout Exception: {}", str(exc))
    else:
        code = HTTPStatus.SERVICE_UNAVAILABLE.value
        msg = HTTPStatus.SERVICE_UNAVAILABLE.description
        detail = str(exc)

    return JSONResponse(
        status_code=code,
        content={
            "code": code,
            "msg": msg,
            "detail": detail,
        },
    )


async def fallback_exception_handler(request: Request, exc: Exception):
    """
    Fallback handler for unhandled exceptions.

    Args:
        request: Request
        exc: Exception

    Returns:
        JSONResponse
    """
    logger_util.full_info("INTERNAL", "Unhandled Exception: {}", str(exc))

    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        content={
            "code": HTTPStatus.INTERNAL_SERVER_ERROR.value,
            "msg": HTTPStatus.INTERNAL_SERVER_ERROR.description,
            "detail": str(exc),
        },
    )