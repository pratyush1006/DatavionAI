"""
Validators for the Patient Preferences module.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError


def validate_timezone(
    value: str,
) -> None:
    """
    Validate timezone.
    """
    if not value.strip():
        raise ValidationError(
            "Timezone cannot be empty.",
        )


def validate_language(
    value: str,
) -> None:
    """
    Validate language.
    """
    if not value.strip():
        raise ValidationError(
            "Language cannot be empty.",
        )


def validate_preferred_name(
    value: str,
) -> None:
    """
    Validate preferred display name.
    """
    if len(value) > 100:
        raise ValidationError(
            "Preferred name cannot exceed 100 characters.",
        )


__all__ = [
    "validate_language",
    "validate_preferred_name",
    "validate_timezone",
]
