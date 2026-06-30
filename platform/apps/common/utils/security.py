import secrets
import string


def generate_random_string(length: int = 12) -> str:
    """
    Generate a cryptographically secure random
    alphanumeric string.
    """

    if length <= 0:
        raise ValueError("Length must be greater than zero.")

    characters = string.ascii_letters + string.digits

    return "".join(secrets.choice(characters) for _ in range(length))
