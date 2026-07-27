"""
Validators for the Emergency Contacts module.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


def validate_emergency_contact_number(
    value: str,
) -> None:
    """
    Validate the emergency contact number.
    """

    if not value:
        raise ValidationError(
            _("Emergency contact number is required."),
        )

    if len(value) > 30:
        raise ValidationError(
            _(
                "Emergency contact number cannot exceed 30 characters.",
            ),
        )


def validate_phone_number(
    value: str,
) -> None:
    """
    Validate a phone number.
    """

    if not value:
        return

    allowed = set("+0123456789 -()")

    if any(character not in allowed for character in value):
        raise ValidationError(
            _("Enter a valid phone number."),
        )

    digits = "".join(character for character in value if character.isdigit())

    if len(digits) < 7 or len(digits) > 15:
        raise ValidationError(
            _(
                "Phone number must contain between 7 and 15 digits.",
            ),
        )


def validate_email_address(
    value: str,
) -> None:
    """
    Validate an email address.
    """

    if not value:
        return

    validate_email(value)


def validate_priority_order(
    value: int,
) -> None:
    """
    Validate the priority order.
    """

    if value < 1:
        raise ValidationError(
            _(
                "Priority order must be greater than zero.",
            ),
        )


def validate_notes(
    value: str,
) -> None:
    """
    Validate notes.
    """

    if not value:
        return

    if len(value) > 2000:
        raise ValidationError(
            _("Notes cannot exceed 2000 characters."),
        )


__all__ = [
    "validate_email_address",
    "validate_emergency_contact_number",
    "validate_notes",
    "validate_phone_number",
    "validate_priority_order",
]
