from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, TypeVar

from django.core.cache import cache

T = TypeVar("T")

_PREFIX = "datavion:ai:circuit"
_OPEN_VALUE = "open"


class DistributedCircuitOpenError(RuntimeError):
    """Raised when a provider circuit is open across workers."""


@dataclass(frozen=True)
class DistributedCircuitConfig:
    failure_threshold: int = 5
    recovery_seconds: int = 60
    key_prefix: str = _PREFIX


def _key(provider: str, config: DistributedCircuitConfig) -> str:
    safe = "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in provider)
    return f"{config.key_prefix}:{safe}"


def _state(provider: str, config: DistributedCircuitConfig) -> dict[str, Any]:
    value = cache.get(_key(provider, config))
    if isinstance(value, dict):
        return value
    return {"failures": 0, "opened_at": None}


def is_open(
    provider: str,
    *,
    config: DistributedCircuitConfig | None = None,
) -> bool:
    config = config or DistributedCircuitConfig()
    state = _state(provider, config)
    opened_at = state.get("opened_at")
    if not opened_at:
        return False
    if time.time() - float(opened_at) >= config.recovery_seconds:
        cache.delete(_key(provider, config))
        return False
    return True


def record_success(
    provider: str,
    *,
    config: DistributedCircuitConfig | None = None,
) -> None:
    config = config or DistributedCircuitConfig()
    cache.delete(_key(provider, config))


def record_failure(
    provider: str,
    *,
    config: DistributedCircuitConfig | None = None,
) -> None:
    config = config or DistributedCircuitConfig()
    key = _key(provider, config)
    state = _state(provider, config)
    failures = int(state.get("failures") or 0) + 1
    opened_at = state.get("opened_at")
    if failures >= config.failure_threshold:
        opened_at = time.time()
    cache.set(
        key,
        {"failures": failures, "opened_at": opened_at},
        timeout=max(config.recovery_seconds, 60),
    )


def call_with_distributed_circuit(
    provider: str,
    func: Callable[[], T],
    *,
    config: DistributedCircuitConfig | None = None,
) -> T:
    config = config or DistributedCircuitConfig()
    if is_open(provider, config=config):
        raise DistributedCircuitOpenError(f"AI provider circuit is open: {provider}")
    try:
        result = func()
    except Exception:
        record_failure(provider, config=config)
        raise
    record_success(provider, config=config)
    return result
