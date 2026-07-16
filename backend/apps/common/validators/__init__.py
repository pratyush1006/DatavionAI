"""
Public validator API for the Datavion AI platform.

Feature applications should import reusable framework
validators from this package.
"""

from __future__ import annotations

from .email import (
    DEFAULT_EMAIL_MESSAGE,
    email_validator,
)
from .phone import (
    DEFAULT_PHONE_NUMBER_MESSAGE,
    PHONE_NUMBER_REGEX,
    phone_number_validator,
)
from .slug import (
    DEFAULT_SLUG_MESSAGE,
    SLUG_REGEX,
)
from .slug import (
    slug_validator as slug_validator,
)

# Backward compatibility
phone_validator = phone_number_validator

__all__ = [
    "DEFAULT_EMAIL_MESSAGE",
    "DEFAULT_PHONE_NUMBER_MESSAGE",
    "DEFAULT_SLUG_MESSAGE",
    "PHONE_NUMBER_REGEX",
    "SLUG_REGEX",
    "email_validator",
    "phone_number_validator",
    "phone_validatorslug_validator",
    "slug_validator",
]
