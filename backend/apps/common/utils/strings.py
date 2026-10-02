"""
String utility functions.

Provides reusable string helpers shared across the
Datavion AI platform.
"""

from __future__ import annotations


def mask_email(
    email: str,
) -> str:
    """
    Mask an email address.

    Examples:
        john@example.com -> jo**@example.com
        ab@example.com   -> **@example.com
    """

    if "@" not in email:
        return email

    username, domain = email.split(
        "@",
        maxsplit=1,
    )

    if len(username) <= 2:
        masked_username = "*" * len(username)
    else:
        masked_username = username[:2] + "*" * (len(username) - 2)

    return f"{masked_username}@{domain}"


def mask_phone_number(
    phone_number: str,
    *,
    visible_digits: int = 4,
) -> str:
    """
    Mask a phone number while preserving the last digits.

    Examples:
        +919876543210 -> ********3210
        9876543210    -> ******3210
    """

    if len(phone_number) <= visible_digits:
        return "*" * len(phone_number)

    return "*" * (len(phone_number) - visible_digits) + phone_number[-visible_digits:]


def normalize_whitespace(
    value: str,
) -> str:
    """
    Collapse consecutive whitespace into a single space.
    """

    return " ".join(
        value.split(),
    )


def truncate(
    value: str,
    *,
    max_length: int,
    suffix: str = "...",
) -> str:
    """
    Truncate a string to the specified maximum length.
    """

    if len(value) <= max_length:
        return value

    return value[: max_length - len(suffix)] + suffix


__all__ = [
    "mask_email",
    "mask_phone_number",
    "normalize_whitespace",
    "truncate",
]
