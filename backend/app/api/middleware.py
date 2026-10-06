"""Rate limiting middleware (in-memory sliding window)."""

import time
from collections import defaultdict, deque

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.config.settings import settings

SENSITIVE_PREFIXES = ("/runtime", "/resume/upload", "/auth/login", "/auth/register")

_buckets: dict = defaultdict(deque)


def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def reset_rate_limit() -> None:
    _buckets.clear()


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not settings.RATE_LIMIT_ENABLED:
            return await call_next(request)
        path = request.url.path
        if path in {"/health", "/ready", "/"}:
            return await call_next(request)
        sensitive = path.startswith(SENSITIVE_PREFIXES)
        limit = (
            settings.RATE_LIMIT_SENSITIVE_PER_MINUTE
            if sensitive
            else settings.RATE_LIMIT_PER_MINUTE
        )
        key = (_client_ip(request), "sensitive" if sensitive else "general")
        now = time.monotonic()
        window = _buckets[key]
        while window and now - window[0] > 60:
            window.popleft()
        if len(window) >= limit:
            return JSONResponse(
                status_code=429,
                content={"error": {"code": "rate_limited",
                                   "message": "Rate limit exceeded. Try again shortly."}},
            )
        window.append(now)
        return await call_next(request)
