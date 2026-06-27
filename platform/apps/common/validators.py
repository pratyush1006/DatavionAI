from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r"^\+?[1-9]\d{9,14}$",
    message="Enter a valid phone number. Example: +919876543210",
)


def validate_organization_code(value: str) -> None:
    """
    Validate that the organization code contains only
    uppercase letters and digits.
    """

    value = value.strip()

    if not value.isalnum():
        raise ValidationError(
            "Organization code may contain only uppercase letters (A-Z) and digits (0-9)."
        )

    if value != value.upper():
        raise ValidationError("Organization code must be uppercase.")
