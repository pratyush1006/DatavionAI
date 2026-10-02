"""
Validators for Patient Family Members.
"""

from __future__ import annotations

import re
from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils import timezone

_NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z\s.'-]{0,99}$")
_PHONE_PATTERN = re.compile(r"^\+?[1-9]\d{7,14}$")


def validate_family_member_name(value: str) -> None:
    value = (value or "").strip()

    if not value:
        raise ValidationError(
            "Name is required.",
            code="required",
        )

    if not _NAME_PATTERN.fullmatch(value):
        raise ValidationError(
            "Enter a valid name.",
            code="invalid_name",
        )


def validate_mobile_number(value: str) -> None:
    value = (value or "").strip()

    if value and not _PHONE_PATTERN.fullmatch(value):
        raise ValidationError(
            "Enter a valid mobile number.",
            code="invalid_mobile_number",
        )


def validate_email_address(value: str) -> None:
    value = (value or "").strip()

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
    if len((value or "").strip()) > 2000:
        raise ValidationError(
            "Notes cannot exceed 2000 characters.",
            code="notes_too_long",
        )


def validate_date_of_birth(value: date | None) -> None:
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
            code="age_too_high",
        )


__all__ = (
    "validate_date_of_birth",
    "validate_email_address",
    "validate_family_member_name",
    "validate_mobile_number",
    "validate_notes",
)
