"""
Validators for the Patient Identifiers module.

These validators enforce the format and integrity of patient identifiers.
They are intentionally reusable across models, serializers, services,
and API layers.
"""

from __future__ import annotations

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

ABHA_PATTERN = re.compile(r"^\d{2}-\d{4}-\d{4}-\d{4}$")
AADHAAR_PATTERN = re.compile(r"^\d{12}$")
PASSPORT_PATTERN = re.compile(r"^[A-Z][0-9]{7}$")
MRN_PATTERN = re.compile(r"^[A-Z0-9\-]{4,30}$")
DRIVING_LICENSE_PATTERN = re.compile(r"^[A-Z0-9\-]{5,30}$")
NATIONAL_ID_PATTERN = re.compile(r"^[A-Z0-9\-]{4,30}$")
INSURANCE_MEMBER_ID_PATTERN = re.compile(r"^[A-Z0-9\-]{4,50}$")
EMPLOYEE_ID_PATTERN = re.compile(r"^[A-Z0-9\-_]{2,30}$")
EXTERNAL_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z0-9_.\-]{1,100}$")


def _validate_pattern(
    value: str,
    pattern: re.Pattern[str],
    message: str,
) -> None:
    """
    Validate a value against a compiled regular expression.
    """

    if not pattern.fullmatch(value):
        raise ValidationError(message)


def validate_mrn(
    value: str,
) -> None:
    """
    Validate a Medical Record Number (MRN).
    """

    _validate_pattern(
        value=value,
        pattern=MRN_PATTERN,
        message=_("Enter a valid Medical Record Number."),
    )


def validate_abha(
    value: str,
) -> None:
    """
    Validate an ABHA number.

    Expected format:
        12-3456-7890-1234
    """

    _validate_pattern(
        value=value,
        pattern=ABHA_PATTERN,
        message=_("Enter a valid ABHA number."),
    )


def validate_aadhaar(
    value: str,
) -> None:
    """
    Validate an Aadhaar number.

    Expected format:
        123412341234
    """

    _validate_pattern(
        value=value,
        pattern=AADHAAR_PATTERN,
        message=_("Enter a valid Aadhaar number."),
    )


def validate_passport(
    value: str,
) -> None:
    """
    Validate a passport number.

    Example:
        A1234567
    """

    _validate_pattern(
        value=value,
        pattern=PASSPORT_PATTERN,
        message=_("Enter a valid passport number."),
    )


def validate_driving_license(
    value: str,
) -> None:
    """
    Validate a driving licence number.
    """

    _validate_pattern(
        value=value,
        pattern=DRIVING_LICENSE_PATTERN,
        message=_("Enter a valid driving licence number."),
    )


def validate_national_id(
    value: str,
) -> None:
    """
    Validate a national identification number.
    """

    _validate_pattern(
        value=value,
        pattern=NATIONAL_ID_PATTERN,
        message=_("Enter a valid national ID."),
    )


def validate_insurance_member_id(
    value: str,
) -> None:
    """
    Validate an insurance member identifier.
    """

    _validate_pattern(
        value=value,
        pattern=INSURANCE_MEMBER_ID_PATTERN,
        message=_("Enter a valid insurance member ID."),
    )


def validate_employee_id(
    value: str,
) -> None:
    """
    Validate an employee identifier.
    """

    _validate_pattern(
        value=value,
        pattern=EMPLOYEE_ID_PATTERN,
        message=_("Enter a valid employee ID."),
    )


def validate_external_identifier(
    value: str,
) -> None:
    """
    Validate identifiers originating from external systems.
    """

    _validate_pattern(
        value=value,
        pattern=EXTERNAL_IDENTIFIER_PATTERN,
        message=_("Enter a valid external identifier."),
    )


__all__ = [
    "validate_aadhaar",
    "validate_abha",
    "validate_driving_license",
    "validate_employee_id",
    "validate_external_identifier",
    "validate_insurance_member_id",
    "validate_mrn",
    "validate_national_id",
    "validate_passport",
]
