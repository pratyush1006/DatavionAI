"""
Organization branding validators.
"""

from __future__ import annotations

import re

from django.core.exceptions import ValidationError

HEX_COLOR_PATTERN = re.compile(
    r"^#[A-Fa-f0-9]{6}$",
)

DOMAIN_PATTERN = re.compile(
    r"^(?=.{1,253}$)(?!-)(?:[a-z0-9-]{1,63}\.)+[a-z]{2,63}$",
    re.IGNORECASE,
)


def validate_hex_color(
    value: str,
) -> None:
    """
    Validate hexadecimal color format (#RRGGBB).
    """

    if not value:
        return

    value = value.strip()

    if not HEX_COLOR_PATTERN.fullmatch(value):
        raise ValidationError(
            "Invalid hexadecimal color format.",
        )


def validate_custom_domain(
    value: str,
) -> None:
    """
    Validate a custom organization domain.
    """

    if not value:
        return

    value = value.strip().lower()

    if not DOMAIN_PATTERN.fullmatch(value):
        raise ValidationError(
            "Invalid custom domain.",
        )


__all__: tuple[str, ...] = (
    "validate_custom_domain",
    "validate_hex_color",
)
