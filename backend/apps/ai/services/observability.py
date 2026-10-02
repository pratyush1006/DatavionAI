"""PHI-safe AI observability primitives."""

from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger("datavion.ai")
_SENSITIVE_KEYS = {
    "prompt",
    "messages",
    "content",
    "text",
    "input",
    "output",
    "response",
    "completion",
    "document",
    "document_content",
    "patient",
    "patient_name",
    "diagnosis",
    "medical_record",
    "clinical_note",
    "prescription",
    "phi",
    "raw_payload",
    "provider_payload",
}


def sanitize_metadata(metadata: dict[str, Any] | None) -> dict[str, Any]:
    if not metadata:
        return {}
    safe: dict[str, Any] = {}
    for key, value in metadata.items():
        k = str(key).strip().lower()
        if k in _SENSITIVE_KEYS or any(
            x in k for x in ("password", "secret", "token", "api_key", "authorization")
        ):
            continue
        if isinstance(value, dict):
            safe[k] = sanitize_metadata(value)
        elif isinstance(value, (list, tuple)):
            safe[k] = [
                sanitize_metadata(x) if isinstance(x, dict) else str(x)[:256]
                for x in value[:20]
            ]
        else:
            safe[k] = (
                value if isinstance(value, (bool, int, float)) else str(value)[:256]
            )
    return safe


def correlation_id(*parts: Any) -> str:
    raw = "|".join("" if p is None else str(p) for p in parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


def safe_exception_reference(exc: Exception) -> str:
    raw = f"{type(exc).__module__}.{type(exc).__name__}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


@dataclass(frozen=True)
class AIRequestMetrics:
    correlation_id: str
    status: str
    latency_ms: int
    provider: str
    model: str
    retry_count: int = 0
    tokens_input: int = 0
    tokens_output: int = 0
    estimated_cost: float = 0.0

    def as_dict(self) -> dict[str, Any]:
        return {
            "correlation_id": self.correlation_id,
            "status": self.status,
            "latency_ms": max(0, int(self.latency_ms)),
            "provider": self.provider,
            "model": self.model,
            "retry_count": max(0, int(self.retry_count)),
            "tokens_input": max(0, int(self.tokens_input)),
            "tokens_output": max(0, int(self.tokens_output)),
            "estimated_cost": max(0.0, float(self.estimated_cost)),
        }


class AIRequestTimer:
    def __init__(self):
        self._started = time.monotonic()

    def elapsed_ms(self) -> int:
        return int((time.monotonic() - self._started) * 1000)


def emit_request_event(event: str, *, metrics: AIRequestMetrics, metadata=None) -> None:
    payload = {
        "event": event,
        "metrics": metrics.as_dict(),
        "metadata": sanitize_metadata(metadata),
    }
    logger.info(
        "ai_event %s", json.dumps(payload, separators=(",", ":"), sort_keys=True)
    )


def emit_failure_event(
    event: str,
    *,
    correlation: str,
    provider: str,
    model: str,
    exc: Exception,
    metadata=None,
) -> None:
    payload = {
        "event": event,
        "correlation_id": correlation,
        "provider": str(provider)[:80],
        "model": str(model)[:160],
        "error_type": type(exc).__name__,
        "error_reference": safe_exception_reference(exc),
        "metadata": sanitize_metadata(metadata),
    }
    logger.warning(
        "ai_failure %s", json.dumps(payload, separators=(",", ":"), sort_keys=True)
    )


def redact_for_log(value: Any) -> str:
    digest = hashlib.sha256(str(value).encode("utf-8")).hexdigest()
    return f"<redacted:{digest[:16]}>"
