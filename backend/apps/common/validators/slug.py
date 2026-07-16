"""
Reusable slug validators.

Provides validators for URL-friendly slugs used across the
Datavion AI platform.
"""

from __future__ import annotations

from django.core.validators import RegexValidator

SLUG_REGEX = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"

DEFAULT_SLUG_MESSAGE = (
    "Enter a valid slug using lowercase letters, numbers, and hyphens only."
)

slug_validator = RegexValidator(
    regex=SLUG_REGEX,
    message=DEFAULT_SLUG_MESSAGE,
)

__all__ = [
    "DEFAULT_SLUG_MESSAGE",
    "SLUG_REGEX",
    "slug_validator",
]
