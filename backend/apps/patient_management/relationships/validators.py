"""
Validators for Patient Relationships.
"""

from __future__ import annotations

import re

from django.core.exceptions import ValidationError

_EXTERNAL_NAME_PATTERN = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9 .,'&()/_-]{0,149}$",
)


def validate_relationship_name(value: str) -> None:
    value = (value or "").strip()

    if not value:
        return

    if not _EXTERNAL_NAME_PATTERN.fullmatch(value):
        raise ValidationError(
            "Enter a valid relationship name.",
            code="invalid_relationship_name",
        )


def validate_relationship_notes(value: str) -> None:
    if value and len(value.strip()) > 5000:
        raise ValidationError(
            "Relationship notes cannot exceed 5000 characters.",
            code="notes_too_long",
        )


def validate_relationship_type(value: str) -> None:
    from apps.patient_management.relationships.constants import (
        RelationshipType,
    )

    if value not in RelationshipType.values:
        raise ValidationError(
            "Invalid relationship type.",
            code="invalid_relationship_type",
        )


__all__ = (
    "validate_relationship_name",
    "validate_relationship_notes",
    "validate_relationship_type",
)
