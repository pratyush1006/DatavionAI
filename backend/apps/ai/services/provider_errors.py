from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderErrorClassification:
    status_code: int | None
    code: str
    error_type: str
    retryable: bool
    quota_exhausted: bool


def classify_provider_error(
    *,
    status_code: int | None = None,
    code: str | None = None,
    error_type: str | None = None,
) -> ProviderErrorClassification:
    normalized_code = (code or "").strip().lower()
    normalized_type = (error_type or "").strip().lower()
    quota_codes = {
        "insufficient_quota",
        "credit_balance_exhausted",
        "billing_hard_limit_reached",
    }
    quota_exhausted = normalized_code in quota_codes or normalized_type in {
        "insufficient_quota",
        "quota_exceeded",
    }
    retryable = (
        status_code in {408, 409, 429, 500, 502, 503, 504} and not quota_exhausted
    )
    return ProviderErrorClassification(
        status_code=status_code,
        code=normalized_code or "unknown",
        error_type=normalized_type or "unknown",
        retryable=retryable,
        quota_exhausted=quota_exhausted,
    )
