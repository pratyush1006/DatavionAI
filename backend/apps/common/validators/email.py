"""
Reusable email address validators.

Provides validators for email addresses used across the
Datavion AI platform.
"""

from __future__ import annotations

from django.core.validators import EmailValidator

DEFAULT_EMAIL_MESSAGE = "Enter a valid email address."

email_validator = EmailValidator(
    message=DEFAULT_EMAIL_MESSAGE,
)

__all__ = [
    "DEFAULT_EMAIL_MESSAGE",
    "email_validator",
]
