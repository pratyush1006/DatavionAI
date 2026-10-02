"""Validation helpers for patient emergency management."""

from __future__ import annotations

from django.core.exceptions import ValidationError


def validate_contact_phone(value: str) -> str:
    """Validate and normalize a contact phone number."""

    normalized = " ".join(str(value).strip().split())

    if len(normalized) < 7:
        raise ValidationError("Emergency contact phone number is too short.")

    return normalized


def validate_contact_name(value: str) -> str:
    """Validate and normalize an emergency contact name."""

    normalized = " ".join(str(value).strip().split())

    if not normalized:
        raise ValidationError("Emergency contact name is required.")

    return normalized


__all__ = (
    "validate_contact_name",
    "validate_contact_phone",
)
