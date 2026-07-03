"""
Reusable phone number validators.

Provides validators for international phone numbers used
across the Datavion AI platform.
"""

from __future__ import annotations

from django.core.validators import RegexValidator

PHONE_NUMBER_REGEX = r"^\+?[1-9]\d{9,14}$"

phone_validator = RegexValidator(
    regex=PHONE_NUMBER_REGEX,
    message=("Enter a valid international phone number. Example: +919876543210."),
)

__all__ = [
    "PHONE_NUMBER_REGEX",
    "phone_validator",
]
