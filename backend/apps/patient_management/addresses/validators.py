"""
Validators for the Addresses module.
"""

from __future__ import annotations

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

POSTAL_CODE_REGEX = re.compile(
    r"^[A-Za-z0-9 -]{3,12}$",
)


def validate_postal_code(
    value: str,
) -> None:
    """Validate a postal code."""
    if not POSTAL_CODE_REGEX.fullmatch(value):
        raise ValidationError(
            _("Enter a valid postal code."),
        )


__all__ = [
    "validate_postal_code",
]
