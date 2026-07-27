"""
Validators for the Patient Consents module.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.utils import timezone

__all__ = [
    "validate_consent_title",
    "validate_effective_date",
    "validate_expiry_date",
    "validate_version",
]


def validate_consent_title(value: str) -> None:
    """
    Validate consent title.
    """

    if not value:
        raise ValidationError(
            "Consent title is required.",
        )

    if len(value.strip()) < 3:
        raise ValidationError(
            "Consent title is too short.",
        )

    if len(value.strip()) > 255:
        raise ValidationError(
            "Consent title cannot exceed 255 characters.",
        )


def validate_version(value: int) -> None:
    """
    Validate consent version.
    """

    if value < 1:
        raise ValidationError(
            "Version must be greater than zero.",
        )


def validate_effective_date(value) -> None:
    """
    Validate effective date.
    """

    if value is None:
        return

    if value < timezone.localdate():
        raise ValidationError(
            "Effective date cannot be in the past.",
        )


def validate_expiry_date(
    effective_date,
    expiry_date,
) -> None:
    """
    Validate expiry date.
    """

    if expiry_date is None:
        return

    if effective_date and expiry_date <= effective_date:
        raise ValidationError(
            "Expiry date must be after the effective date.",
        )
