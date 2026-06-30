from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r"^\+?[1-9]\d{9,14}$",
    message="Enter a valid phone number. Example: +919876543210",
)
