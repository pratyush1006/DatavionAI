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


__all__ = [
    "mask_email",
]
