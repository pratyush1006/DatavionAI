"""
Validators for the Master Patient Index (MPI) module.
"""

from __future__ import annotations

import re

from django.core.exceptions import ValidationError

MPI_ID_PATTERN = re.compile(
    r"^[A-Z]{3}-[0-9]{10}$",
)

ABHA_PATTERN = re.compile(
    r"^\d{2}-\d{4}-\d{4}-\d{4}$",
)

AADHAAR_PATTERN = re.compile(
    r"^\d{12}$",
)

PASSPORT_PATTERN = re.compile(
    r"^[A-Z][0-9]{7}$",
)


def validate_mpi_id(
    value: str,
) -> None:
    """
    Validate a Datavion MPI identifier.
    """
    if not MPI_ID_PATTERN.fullmatch(
        value,
    ):
        raise ValidationError(
            "Invalid MPI identifier format.",
        )


def validate_abha_number(
    value: str,
) -> None:
    """
    Validate an ABHA number.
    """
    if not ABHA_PATTERN.fullmatch(
        value,
    ):
        raise ValidationError(
            "Invalid ABHA number.",
        )


def validate_aadhaar_number(
    value: str,
) -> None:
    """
    Validate an Aadhaar number.
    """
    if not AADHAAR_PATTERN.fullmatch(
        value,
    ):
        raise ValidationError(
            "Invalid Aadhaar number.",
        )


def validate_passport_number(
    value: str,
) -> None:
    """
    Validate a passport number.
    """
    if not PASSPORT_PATTERN.fullmatch(
        value,
    ):
        raise ValidationError(
            "Invalid passport number.",
        )


__all__ = [
    "validate_aadhaar_number",
    "validate_abha_number",
    "validate_mpi_id",
    "validate_passport_number",
]
