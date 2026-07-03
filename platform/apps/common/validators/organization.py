"""
Reusable organization validators.

Provides validators shared across the Datavion AI platform
for organization-related fields.
"""

from __future__ import annotations

import re

from django.core.exceptions import ValidationError

ORGANIZATION_CODE_PATTERN = re.compile(
    r"^[A-Z0-9]+$",
)


def validate_organization_code(
    value: str,
) -> None:
    """
    Validate an organization code.

    Rules:
    - Must contain only uppercase letters (A-Z) and digits (0-9).
    - Must not contain spaces or special characters.
    """

    value = value.strip()

    if not value:
        raise ValidationError(
            "Organization code cannot be empty.",
        )

    if not ORGANIZATION_CODE_PATTERN.fullmatch(
        value,
    ):
        raise ValidationError(
            (
                "Organization code may contain only "
                "uppercase letters (A-Z) and digits (0-9)."
            ),
        )


__all__ = [
    "ORGANIZATION_CODE_PATTERN",
    "validate_organization_code",
]
