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
