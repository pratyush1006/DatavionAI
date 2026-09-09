"""Idempotency primitives for financial operations."""

from __future__ import annotations

import hashlib


def normalize_idempotency_key(value: str) -> str:
    """Normalize an external idempotency key."""
    normalized = value.strip()
    if not normalized:
        raise ValueError("Idempotency key cannot be empty.")
    return normalized


def idempotency_fingerprint(*, operation: str, key: str) -> str:
    """Create a stable operation/key fingerprint."""
    payload = f"{operation.strip()}:{normalize_idempotency_key(key)}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


__all__ = ["idempotency_fingerprint", "normalize_idempotency_key"]
