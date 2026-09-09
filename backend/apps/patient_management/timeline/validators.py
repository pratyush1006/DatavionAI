"""
Validation helpers for Patient Timeline.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError


def validate_timeline_title(value: str) -> None:
    """Validate a timeline entry title."""

    if value is None:
        return

    if not value.strip():
        raise ValidationError("Timeline title cannot be blank.")


__all__ = ("validate_timeline_title",)
