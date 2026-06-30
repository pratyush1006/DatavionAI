from django.core.exceptions import ValidationError


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
