"""
Reusable email address validators.

Provides reusable email validation utilities for DatavionOS.
"""

from __future__ import annotations

from django.core.validators import (
    EmailValidator,
)

DEFAULT_EMAIL_MESSAGE = "Enter a valid email address."


def create_email_validator(
    *,
    message: str = DEFAULT_EMAIL_MESSAGE,
) -> EmailValidator:
    """
    Create an email validator.

    Args:
        message:
            Validation error message.

    Returns:
        Configured EmailValidator instance.
    """

    return EmailValidator(
        message=message,
    )


email_validator = create_email_validator()


def validate_email(
    value: str,
) -> None:
    """
    Validate an email address.

    Raises:
        ValidationError:
            If email format is invalid.
    """

    email_validator(
        value,
    )


__all__ = (
    "DEFAULT_EMAIL_MESSAGE",
    "create_email_validator",
    "email_validator",
    "validate_email",
)
