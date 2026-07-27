"""
Validators for the Family Members module.
"""

from __future__ import annotations

import re

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils import timezone

__all__ = [
    "validate_family_member_name",
    "validate_mobile_number",
    "validate_email_address",
    "validate_notes",
    "validate_date_of_birth",
]


_NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z\s.'-]{0,99}$")
_PHONE_PATTERN = re.compile(r"^\+?[1-9]\d{7,14}$")


def validate_family_member_name(value: str) -> None:
    """
    Validate a family member's name.
    """
    if not value:
        raise ValidationError(
            "Name is required.",
            code="required",
        )

    value = value.strip()

    if not _NAME_PATTERN.fullmatch(value):
        raise ValidationError(
            "Enter a valid name.",
            code="invalid_name",
        )


def validate_mobile_number(value: str) -> None:
    """
    Validate an international mobile number.
    """
    if not value:
        return

    value = value.strip()

    if not _PHONE_PATTERN.fullmatch(value):
        raise ValidationError(
            "Enter a valid mobile number.",
            code="invalid_mobile_number",
        )


def validate_email_address(value: str) -> None:
    """
    Validate an email address.
    """
    if not value:
        return

    try:
        validate_email(value)
    except ValidationError as exc:
        raise ValidationError(
            "Enter a valid email address.",
            code="invalid_email",
        ) from exc


def validate_notes(value: str) -> None:
    """
    Validate notes length.
    """
    if not value:
        return

    if len(value.strip()) > 1000:
        raise ValidationError(
            "Notes cannot exceed 1000 characters.",
            code="notes_too_long",
        )


def validate_date_of_birth(value) -> None:
    """
    Validate date of birth.
    """
    if value is None:
        return

    today = timezone.localdate()

    if value > today:
        raise ValidationError(
            "Date of birth cannot be in the future.",
            code="future_date",
        )

    age = (
        today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    )

    if age > 130:
        raise ValidationError(
            "Age cannot exceed 130 years.",
            code="invalid_age",
        )
