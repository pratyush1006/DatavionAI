from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r"^\+?[1-9]\d{9,14}$",
    message=("Enter a valid phone number. " "Example: +919876543210"),
)


def validate_organization_code(value):
    """
    Organization code must contain only
    uppercase letters and numbers.
    """

    if not value.isalnum():
        raise ValidationError(
            "Organization code must contain only letters and numbers."
        )

    if value != value.upper():
        raise ValidationError("Organization code must be uppercase.")
