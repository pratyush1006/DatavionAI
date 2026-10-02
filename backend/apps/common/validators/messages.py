"""
DatavionAI Validation Messages.

Centralized validation messages.

Design Principles
-----------------
- Immutable
- Consistent
- Reusable
- Localization ready
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Final

###############################################################################
# Default Messages
###############################################################################

VALIDATION_MESSAGES: Final = MappingProxyType(
    {
        # Generic
        "required": "This field is required.",
        "invalid": "Invalid value.",
        "blank": "This field cannot be blank.",
        "null": "This field cannot be null.",
        # Length
        "min_length": "Ensure this value has at least {min_length} characters.",
        "max_length": "Ensure this value has at most {max_length} characters.",
        "exact_length": "Ensure this value has exactly {length} characters.",
        # Numeric
        "min_value": "Ensure this value is greater than or equal to {min_value}.",
        "max_value": "Ensure this value is less than or equal to {max_value}.",
        # String
        "invalid_choice": "Select a valid choice.",
        "invalid_format": "Invalid format.",
        # UUID
        "invalid_uuid": "Enter a valid UUID.",
        # Email
        "invalid_email": "Enter a valid email address.",
        # Phone
        "invalid_phone": "Enter a valid phone number.",
        # URL
        "invalid_url": "Enter a valid URL.",
        # Slug
        "invalid_slug": "Enter a valid slug.",
        # Password
        "weak_password": "Password does not meet security requirements.",
        # File
        "invalid_file": "Invalid file.",
        "file_too_large": "File exceeds the maximum allowed size.",
        "unsupported_file_type": "Unsupported file type.",
        # Date & Time
        "invalid_date": "Enter a valid date.",
        "invalid_datetime": "Enter a valid date and time.",
        "invalid_time": "Enter a valid time.",
        # Business
        "already_exists": "Object already exists.",
        "not_found": "Object not found.",
        "inactive": "Object is inactive.",
        "permission_denied": "Permission denied.",
    }
)

###############################################################################
# Helper
###############################################################################


def get_message(
    key: str,
    **kwargs: object,
) -> str:
    """
    Return a formatted validation message.

    Falls back to the key itself if no message
    is registered.
    """

    message = VALIDATION_MESSAGES.get(
        key,
        key,
    )

    return message.format(
        **kwargs,
    )


###############################################################################
# Public Exports
###############################################################################

__all__ = (
    "VALIDATION_MESSAGES",
    "get_message",
)
