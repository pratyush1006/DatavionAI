"""
Validators for the Contacts module.
"""

from __future__ import annotations

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

PHONE_REGEX = re.compile(r"^\+?[1-9]\d{7,14}$")
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
)


def validate_phone_number(value: str) -> None:
    """Validate an international phone number."""
    if not PHONE_REGEX.fullmatch(value):
        raise ValidationError(
            _("Enter a valid phone number."),
        )


def validate_email_address(value: str) -> None:
    """Validate an email address."""
    if not EMAIL_REGEX.fullmatch(value):
        raise ValidationError(
            _("Enter a valid email address."),
        )


__all__ = [
    "validate_email_address",
    "validate_phone_number",
]
