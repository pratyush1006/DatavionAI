"""
Validators for the Patient Relationships module.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError


def validate_relationship_notes(
    value: str,
) -> None:
    """
    Validate relationship notes.
    """
    if len(value) > 2000:
        raise ValidationError(
            "Relationship notes cannot exceed 2000 characters.",
        )


def validate_relationship_strength(
    value: int,
) -> None:
    """
    Validate relationship strength.
    """
    if value < 1 or value > 10:
        raise ValidationError(
            "Relationship strength must be between 1 and 10.",
        )


__all__ = [
    "validate_relationship_notes",
    "validate_relationship_strength",
]
