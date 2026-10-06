"""Consistent API error model.

All failures return ``{"error": {"code": ..., "message": ...}}`` with an
appropriate HTTP status code. Internal exception details are never exposed.
"""

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("skilltwin")


class ApiError(StarletteHTTPException):
    def __init__(self, status_code: int, code: str, message: str):
        super().__init__(status_code=status_code, detail=message)
        self.code = code


def bad_request(message: str) -> ApiError:
    return ApiError(400, "bad_request", message)


def unauthorized(message: str = "Authentication required.") -> ApiError:
    return ApiError(401, "unauthorized", message)


def forbidden(message: str = "Access denied.") -> ApiError:
    return ApiError(403, "forbidden", message)


def not_found(resource: str = "Resource") -> ApiError:
    return ApiError(404, "not_found", f"{resource} not found.")


def conflict(message: str) -> ApiError:
    return ApiError(409, "conflict", message)


def payload_too_large(message: str) -> ApiError:
    return ApiError(413, "payload_too_large", message)


def too_many_requests(message: str = "Rate limit exceeded. Try again shortly.") -> ApiError:
    return ApiError(429, "rate_limited", message)


def service_unavailable(message: str) -> ApiError:
    return ApiError(503, "service_unavailable", message)


def _error_payload(code: str, message: str) -> dict:
    return {"error": {"code": code, "message": message}}


async def _api_error_handler(_: Request, exc: ApiError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_payload(exc.code, str(exc.detail)),
    )


async def _http_error_handler(_: Request, exc: StarletteHTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_payload("http_error", str(exc.detail)),
    )


async def _validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    first = exc.errors()[0] if exc.errors() else {}
    field = ".".join(str(part) for part in first.get("loc", []) if part != "body")
    message = first.get("msg", "Invalid request.")
    if field:
        message = f"{field}: {message}"
    return JSONResponse(status_code=422, content=_error_payload("validation_error", message))


async def _unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content=_error_payload("internal_error", "An unexpected error occurred."),
    )


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApiError, _api_error_handler)
    app.add_exception_handler(StarletteHTTPException, _http_error_handler)
    app.add_exception_handler(RequestValidationError, _validation_error_handler)
    app.add_exception_handler(Exception, _unhandled_error_handler)
