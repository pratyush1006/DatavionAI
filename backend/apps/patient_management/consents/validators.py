"""
Validation helpers for Patient Consents.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_consent_dates(
    *,
    expires_at=None,
    granted_at=None,
) -> None:
    """
    Validate chronological Patient Consent timestamps.
    """
    if expires_at is not None and granted_at is not None:
        if expires_at <= granted_at:
            raise ValidationError(
                "Consent expiration must occur after consent grant time.",
            )

    if expires_at is not None and expires_at <= timezone.now():
        raise ValidationError(
            "Consent expiration must be in the future.",
        )


def validate_consent_notes(
    value: str,
) -> str:
    """
    Normalize consent notes and reject excessively large values.
    """
    normalized = str(
        value or "",
    ).strip()

    if len(normalized) > 10000:
        raise ValidationError(
            "Consent notes cannot exceed 10,000 characters.",
        )

    return normalized


__all__ = (
    "validate_consent_dates",
    "validate_consent_notes",
)
