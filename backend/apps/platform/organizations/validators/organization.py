"""
Reusable organization validators.

Provides validators shared across the DatavionAI platform
for organization-related fields.
"""

from __future__ import annotations

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

MIN_ORGANIZATION_CODE_LENGTH = 2

MAX_ORGANIZATION_CODE_LENGTH = 20

ORGANIZATION_CODE_PATTERN = re.compile(
    r"^[A-Z0-9]+$",
)


def validate_organization_code(
    value: str,
) -> None:
    """
    Validate an organization code.

    Rules
    -----
    - Required.
    - 2–20 characters.
    - Uppercase letters (A-Z) and digits (0-9) only.
    - No spaces.
    - No special characters.
    """

    value = value.strip()

    if not value:
        raise ValidationError(
            _(
                "Organization code cannot be empty.",
            ),
        )

    if len(value) < MIN_ORGANIZATION_CODE_LENGTH:
        raise ValidationError(
            _("Organization code must contain at least %(length)s characters."),
            params={
                "length": MIN_ORGANIZATION_CODE_LENGTH,
            },
        )

    if len(value) > MAX_ORGANIZATION_CODE_LENGTH:
        raise ValidationError(
            _("Organization code cannot exceed %(length)s characters."),
            params={
                "length": MAX_ORGANIZATION_CODE_LENGTH,
            },
        )

    if not ORGANIZATION_CODE_PATTERN.fullmatch(
        value,
    ):
        raise ValidationError(
            _(
                "Organization code may contain only "
                "uppercase letters (A-Z) and digits (0-9)."
            ),
        )


__all__ = [
    "MAX_ORGANIZATION_CODE_LENGTH",
    "MIN_ORGANIZATION_CODE_LENGTH",
    "ORGANIZATION_CODE_PATTERN",
    "validate_organization_code",
]
