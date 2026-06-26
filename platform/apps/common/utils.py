import random
import string


def generate_code(prefix="", length=6):
    """
    Generate an uppercase code.

    Example:
        DAT-AB12CD
    """

    characters = string.ascii_uppercase + string.digits

    random_part = "".join(
        random.choices(characters, k=length)
    )

    if prefix:
        return f"{prefix}-{random_part}"

    return random_part


def generate_random_string(length=12):
    """
    Generate a random string.
    """

    characters = (
        string.ascii_letters
        + string.digits
    )

    return "".join(
        random.choice(characters)
        for _ in range(length)
    )


def mask_email(email):
    """
    Example:
    john@example.com

    becomes

    jo****@example.com
    """

    if "@" not in email:
        return email

    username, domain = email.split("@")

    if len(username) <= 2:
        return "*" * len(username) + "@" + domain

    return (
        username[:2]
        + "*" * (len(username) - 2)
        + "@"
        + domain
    )