from __future__ import annotations

import pytest

from api.rate_limit import FixedWindowRateLimiter


class ManualClock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


def test_fixed_window_rate_limiter_allows_up_to_limit_then_blocks() -> None:
    clock = ManualClock()
    limiter = FixedWindowRateLimiter(limit=2, window_seconds=60, clock=clock)

    first = limiter.check("client")
    second = limiter.check("client")
    third = limiter.check("client")

    assert first.allowed is True
    assert first.remaining == 1
    assert second.allowed is True
    assert second.remaining == 0
    assert third.allowed is False
    assert third.retry_after_seconds == 60


def test_fixed_window_rate_limiter_resets_after_window_expires() -> None:
    clock = ManualClock()
    limiter = FixedWindowRateLimiter(limit=1, window_seconds=60, clock=clock)

    assert limiter.check("client").allowed is True
    assert limiter.check("client").allowed is False

    clock.now = 60.0

    result = limiter.check("client")

    assert result.allowed is True
    assert result.remaining == 0


def test_fixed_window_rate_limiter_tracks_clients_independently() -> None:
    limiter = FixedWindowRateLimiter(limit=1, window_seconds=60)

    assert limiter.check("client-a").allowed is True
    assert limiter.check("client-a").allowed is False
    assert limiter.check("client-b").allowed is True


def test_fixed_window_rate_limiter_rejects_invalid_configuration() -> None:
    with pytest.raises(ValueError):
        FixedWindowRateLimiter(limit=0, window_seconds=60)

    with pytest.raises(ValueError):
        FixedWindowRateLimiter(limit=1, window_seconds=0)
