"""
Validators for the Patient Registration module.
"""

from __future__ import annotations

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

REGISTRATION_NUMBER_PATTERN = re.compile(
    r"^[A-Z]{2,10}-[A-Z0-9]{1,10}-\d{4,10}$",
)


def validate_registration_number(
    value: str,
) -> None:
    """
    Validate the registration number format.

    Expected examples:
    - REG-2026-000001
    - BLR-REG-000001
    """

    if not value:
        raise ValidationError(
            _("Registration number is required."),
        )

    if not REGISTRATION_NUMBER_PATTERN.fullmatch(value):
        raise ValidationError(
            _(
                "Invalid registration number format.",
            ),
        )


def validate_notes(
    value: str,
) -> None:
    """
    Validate registration notes.
    """

    if not value:
        return

    if len(value) > 5000:
        raise ValidationError(
            _(
                "Notes cannot exceed 5000 characters.",
            ),
        )


def validate_cancellation_reason(
    value: str,
) -> None:
    """
    Validate cancellation reason.
    """

    if not value:
        raise ValidationError(
            _(
                "Cancellation reason is required.",
            ),
        )

    if len(value.strip()) < 5:
        raise ValidationError(
            _(
                "Cancellation reason is too short.",
            ),
        )

    if len(value) > 1000:
        raise ValidationError(
            _(
                "Cancellation reason cannot exceed 1000 characters.",
            ),
        )
