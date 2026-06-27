"""
Common utility functions used across DatavionAI.
"""

import secrets
import string


def generate_code(
    prefix: str = "",
    length: int = 6,
) -> str:
    """
    Generate a random uppercase alphanumeric code.

    Example:
        DAT-AB12CD
    """

    if length <= 0:
        raise ValueError("Length must be greater than zero.")

    characters = string.ascii_uppercase + string.digits

    random_part = "".join(secrets.choice(characters) for _ in range(length))

    if prefix:
        return f"{prefix}-{random_part}"

    return random_part


def generate_random_string(length: int = 12) -> str:
    """
    Generate a cryptographically secure random
    alphanumeric string.
    """

    if length <= 0:
        raise ValueError("Length must be greater than zero.")

    characters = string.ascii_letters + string.digits

    return "".join(secrets.choice(characters) for _ in range(length))


def mask_email(email: str) -> str:
    """
    Mask an email address.

    Example:
        john@example.com

    becomes

        jo**@example.com
    """

    if "@" not in email:
        return email

    username, domain = email.split("@", 1)

    if len(username) <= 2:
        return "*" * len(username) + "@" + domain

    return username[:2] + "*" * (len(username) - 2) + "@" + domain
