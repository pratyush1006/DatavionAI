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
