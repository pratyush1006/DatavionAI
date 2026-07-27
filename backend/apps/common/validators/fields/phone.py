"""
Reusable phone number validators.

Provides reusable validation utilities for international phone
numbers used throughout DatavionOS.

Phone numbers are validated using Google's libphonenumber
(via the phonenumbers package), which supports numbering
plans for more than 240 countries and territories.
"""

from __future__ import annotations

import phonenumbers
from django.core.exceptions import ValidationError

DEFAULT_PHONE_NUMBER_MESSAGE = "Enter a valid international phone number."


def validate_phone_number(
    value: str,
) -> None:
    """
    Validate an international phone number.

    The supplied value should preferably be in E.164 format,
    for example:

        +14155552671
        +919876543210

    Args:
        value:
            Phone number to validate.

    Raises:
        ValidationError:
            If the phone number is invalid.
    """

    try:
        number = phonenumbers.parse(
            value,
            region=None,
        )
    except phonenumbers.NumberParseException as exc:
        raise ValidationError(
            DEFAULT_PHONE_NUMBER_MESSAGE,
        ) from exc

    if not phonenumbers.is_possible_number(number):
        raise ValidationError(
            DEFAULT_PHONE_NUMBER_MESSAGE,
        )

    if not phonenumbers.is_valid_number(number):
        raise ValidationError(
            DEFAULT_PHONE_NUMBER_MESSAGE,
        )


phone_number_validator = validate_phone_number

phone_validator = validate_phone_number


def normalize_phone_number(
    value: str,
) -> str:
    """
    Normalize a phone number to E.164 format.

    Args:
        value:
            Phone number to normalize.

    Returns:
        Normalized phone number.

    Raises:
        ValidationError:
            If the phone number is invalid.
    """

    validate_phone_number(value)

    number = phonenumbers.parse(
        value,
        region=None,
    )

    return phonenumbers.format_number(
        number,
        phonenumbers.PhoneNumberFormat.E164,
    )


__all__ = (
    "DEFAULT_PHONE_NUMBER_MESSAGE",
    "normalize_phone_number",
    "phone_number_validator",
    "phone_validator",
    "validate_phone_number",
)
