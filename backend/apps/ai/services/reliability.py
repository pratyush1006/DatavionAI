"""Production reliability primitives for DatavionAI."""

from __future__ import annotations

import hashlib
import threading
import time
from collections import defaultdict
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeoutError
from dataclasses import dataclass
from typing import TypeVar

from django.core.cache import cache

from apps.ai.exceptions import AIProviderError, AIProviderUnavailable
from apps.ai.providers import ChatRequest, ChatResponse

T = TypeVar("T")


@dataclass(frozen=True)
class ReliabilityConfig:
    timeout_seconds: int = 30
    retry_count: int = 2
    retry_backoff_seconds: float = 0.5
    circuit_failure_threshold: int = 5
    circuit_open_seconds: int = 30
    idempotency_lock_seconds: int = 120


class CircuitOpenError(AIProviderError):
    """Raised when a provider circuit is open."""


@dataclass
class _CircuitState:
    failures: int = 0
    opened_at: float = 0.0


_CIRCUITS: dict[str, _CircuitState] = defaultdict(_CircuitState)
_CIRCUIT_LOCK = threading.RLock()


def _config() -> ReliabilityConfig:
    from apps.ai.production import production_config

    cfg = production_config()
    return ReliabilityConfig(
        timeout_seconds=cfg.timeout_seconds,
        retry_count=cfg.retry_count,
    )


def _key(provider_name: str, model: str) -> str:
    return f"{provider_name}:{model}"


def _open(key: str, cfg: ReliabilityConfig) -> bool:
    with _CIRCUIT_LOCK:
        state = _CIRCUITS[key]
        if not state.opened_at:
            return False
        if time.monotonic() - state.opened_at >= cfg.circuit_open_seconds:
            _CIRCUITS[key] = _CircuitState()
            return False
        return True


def _success(key: str) -> None:
    with _CIRCUIT_LOCK:
        _CIRCUITS[key] = _CircuitState()


def _failure(key: str, cfg: ReliabilityConfig) -> None:
    with _CIRCUIT_LOCK:
        state = _CIRCUITS[key]
        state.failures += 1
        if state.failures >= cfg.circuit_failure_threshold:
            state.opened_at = time.monotonic()


def _bounded_call(callback: Callable[[], T], timeout_seconds: int) -> T:
    with ThreadPoolExecutor(
        max_workers=1, thread_name_prefix="datavion-ai"
    ) as executor:
        future = executor.submit(callback)
        try:
            return future.result(timeout=timeout_seconds)
        except FutureTimeoutError as exc:
            future.cancel()
            raise AIProviderError("AI provider timeout") from exc


def complete_with_reliability(
    *,
    provider,
    request: ChatRequest,
    provider_name: str,
    model: str,
) -> ChatResponse:
    cfg = _config()
    key = _key(provider_name, model)

    if _open(key, cfg):
        raise CircuitOpenError(f"AI provider circuit is open: {provider_name}")

    for attempt in range(cfg.retry_count + 1):
        try:
            response = _bounded_call(
                lambda: provider.complete(request),
                cfg.timeout_seconds,
            )
            _success(key)
            return response
        except (AIProviderUnavailable, AIProviderError):
            _failure(key, cfg)
            if attempt >= cfg.retry_count:
                raise
            time.sleep(cfg.retry_backoff_seconds * (2**attempt))
        except Exception as exc:
            _failure(key, cfg)
            if attempt >= cfg.retry_count:
                raise AIProviderError(str(exc)) from exc
            time.sleep(cfg.retry_backoff_seconds * (2**attempt))

    raise AIProviderError("AI provider failed")


def request_fingerprint(
    *,
    tenant_id,
    organization_id,
    application_id,
    module_reference_id,
    provider_name: str,
    model: str,
    messages,
    temperature: float,
    max_tokens: int,
    idempotency_key: str,
) -> str:
    payload = repr(
        {
            "tenant": str(tenant_id),
            "organization": str(organization_id),
            "application": str(application_id),
            "module_reference": str(module_reference_id),
            "provider": provider_name,
            "model": model,
            "messages": list(messages),
            "temperature": float(temperature),
            "max_tokens": int(max_tokens),
            "idempotency_key": idempotency_key,
        }
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def acquire_idempotency_lock(fingerprint: str, seconds: int) -> bool:
    return bool(
        cache.add(
            f"datavion:ai:idempotency:{fingerprint}",
            "locked",
            timeout=seconds,
        )
    )


def release_idempotency_lock(fingerprint: str) -> None:
    cache.delete(f"datavion:ai:idempotency:{fingerprint}")
