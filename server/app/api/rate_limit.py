from __future__ import annotations

import math
import time
from dataclasses import dataclass
from threading import Lock
from typing import Callable

from fastapi import HTTPException, Request, Response

from core.config import get_settings


Clock = Callable[[], float]


@dataclass(frozen=True)
class RateLimitResult:
    allowed: bool
    limit: int
    remaining: int
    retry_after_seconds: int


class FixedWindowRateLimiter:
    """Small in-memory fixed-window limiter for per-process API protection."""

    def __init__(self, limit: int, window_seconds: int, clock: Clock = time.monotonic) -> None:
        if limit < 1:
            raise ValueError("limit must be at least 1")
        if window_seconds < 1:
            raise ValueError("window_seconds must be at least 1")

        self.limit = limit
        self.window_seconds = window_seconds
        self._clock = clock
        self._lock = Lock()
        self._windows: dict[str, tuple[float, int]] = {}

    def check(self, key: str) -> RateLimitResult:
        now = self._clock()

        with self._lock:
            window_start, count = self._windows.get(key, (now, 0))

            if now - window_start >= self.window_seconds:
                window_start = now
                count = 0

            retry_after = max(1, math.ceil(self.window_seconds - (now - window_start)))

            if count >= self.limit:
                return RateLimitResult(
                    allowed=False,
                    limit=self.limit,
                    remaining=0,
                    retry_after_seconds=retry_after,
                )

            count += 1
            self._windows[key] = (window_start, count)

            return RateLimitResult(
                allowed=True,
                limit=self.limit,
                remaining=self.limit - count,
                retry_after_seconds=retry_after,
            )

    def reset(self) -> None:
        with self._lock:
            self._windows.clear()


settings = get_settings()
search_rate_limiter = FixedWindowRateLimiter(
    limit=settings.search_rate_limit_per_minute,
    window_seconds=60,
)
tags_rate_limiter = FixedWindowRateLimiter(
    limit=settings.tags_rate_limit_per_minute,
    window_seconds=60,
)


def _client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"


def _apply_rate_limit_headers(response: Response, result: RateLimitResult) -> None:
    response.headers["X-RateLimit-Limit"] = str(result.limit)
    response.headers["X-RateLimit-Remaining"] = str(result.remaining)
    response.headers["X-RateLimit-Reset"] = str(result.retry_after_seconds)


def rate_limit_dependency(
    limiter: FixedWindowRateLimiter,
    scope: str,
) -> Callable[[Request, Response], None]:
    def enforce_rate_limit(request: Request, response: Response) -> None:
        key = f"{scope}:{_client_ip(request)}"
        result = limiter.check(key)

        if result.allowed:
            _apply_rate_limit_headers(response, result)
            return

        headers = {
            "Retry-After": str(result.retry_after_seconds),
            "X-RateLimit-Limit": str(result.limit),
            "X-RateLimit-Remaining": "0",
            "X-RateLimit-Reset": str(result.retry_after_seconds),
        }
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please retry later.",
            headers=headers,
        )

    return enforce_rate_limit


def reset_rate_limiters() -> None:
    search_rate_limiter.reset()
    tags_rate_limiter.reset()
