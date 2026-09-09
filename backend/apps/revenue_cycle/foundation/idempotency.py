"""Revenue Cycle idempotency helpers."""

from __future__ import annotations

from hashlib import sha256

from apps.revenue_cycle.exceptions import RevenueCycleIdempotencyError

MAX_IDEMPOTENCY_KEY_LENGTH = 255


def normalize_idempotency_key(value: str) -> str:
    """Validate and normalize an external idempotency key."""
    normalized = str(value).strip()

    if not normalized:
        raise RevenueCycleIdempotencyError("Idempotency key cannot be empty.")

    if len(normalized) > MAX_IDEMPOTENCY_KEY_LENGTH:
        raise RevenueCycleIdempotencyError(
            "Idempotency key exceeds the maximum length."
        )

    return normalized


def fingerprint_idempotency_key(
    *,
    operation: str,
    key: str,
) -> str:
    """Create a deterministic operation/key fingerprint."""
    normalized_key = normalize_idempotency_key(key)
    payload = f"{operation.strip().lower()}:{normalized_key}"

    return sha256(payload.encode("utf-8")).hexdigest()


__all__ = (
    "fingerprint_idempotency_key",
    "normalize_idempotency_key",
)
