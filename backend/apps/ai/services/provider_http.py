from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from django.conf import settings


@dataclass(frozen=True)
class ProviderHTTPConfig:
    connect_timeout: float
    read_timeout: float
    total_timeout: float
    retries: int


def _positive_float(name: str, default: float) -> float:
    try:
        value = float(getattr(settings, name, default))
    except (TypeError, ValueError):
        value = default
    return max(value, 0.1)


def _nonnegative_int(name: str, default: int) -> int:
    try:
        value = int(getattr(settings, name, default))
    except (TypeError, ValueError):
        value = default
    return max(value, 0)


def provider_http_config() -> ProviderHTTPConfig:
    total = _positive_float(
        "AI_PROVIDER_TIMEOUT_SECONDS",
        _positive_float("AI_HTTP_TIMEOUT_SECONDS", 30.0),
    )
    connect = min(
        _positive_float("AI_HTTP_CONNECT_TIMEOUT_SECONDS", 5.0),
        total,
    )
    read = min(
        _positive_float("AI_HTTP_READ_TIMEOUT_SECONDS", total),
        total,
    )
    retries = _nonnegative_int(
        "AI_PROVIDER_RETRY_COUNT",
        _nonnegative_int("AI_HTTP_RETRY_COUNT", 2),
    )
    return ProviderHTTPConfig(
        connect_timeout=connect,
        read_timeout=read,
        total_timeout=total,
        retries=retries,
    )


def requests_timeout() -> tuple[float, float]:
    config = provider_http_config()
    return config.connect_timeout, config.read_timeout


def httpx_timeout_kwargs() -> dict[str, float]:
    config = provider_http_config()
    return {
        "connect": config.connect_timeout,
        "read": config.read_timeout,
        "write": config.total_timeout,
        "pool": config.connect_timeout,
    }


def provider_call_kwargs() -> dict[str, Any]:
    config = provider_http_config()
    return {
        "timeout": config.total_timeout,
        "retries": config.retries,
    }
