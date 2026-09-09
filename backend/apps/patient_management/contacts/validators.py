"""
Validators for the Patient Contacts module.

Validation policy
-----------------
- Phone-based contact types use international phone validation.
- Email contacts use email validation.
- OTHER contacts accept normalized non-empty text.
"""

from __future__ import annotations

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

PHONE_REGEX = re.compile(
    r"^\+?[1-9]\d{7,14}$",
)

EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
)


def validate_phone_number(
    value: str,
) -> None:
    """
    Validate an international phone number.

    The canonical format is compatible with E.164-style values while
    remaining intentionally permissive about the leading ``+``.
    """
    normalized = str(value).strip()

    if not PHONE_REGEX.fullmatch(normalized):
        raise ValidationError(
            _("Enter a valid phone number."),
        )


def validate_email_address(
    value: str,
) -> None:
    """
    Validate an email address.
    """
    normalized = str(value).strip()

    if not EMAIL_REGEX.fullmatch(normalized):
        raise ValidationError(
            _("Enter a valid email address."),
        )


def validate_contact_value(
    value: str,
) -> None:
    """
    Validate a generic contact value.

    OTHER contact types are deliberately treated as opaque text because
    the domain does not define a specific machine-readable format for them.
    """
    normalized = str(value).strip()

    if not normalized:
        raise ValidationError(
            _("Contact value cannot be empty."),
        )

    if len(normalized) > 255:
        raise ValidationError(
            _("Contact value cannot exceed 255 characters."),
        )


__all__ = (
    "validate_contact_value",
    "validate_email_address",
    "validate_phone_number",
)
