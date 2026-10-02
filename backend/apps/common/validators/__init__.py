"""
DatavionOS reusable validators.

Provides the public validation API used across the platform.

Application modules should import validators from this package instead of
internal validator modules.
"""

from __future__ import annotations

from .base import (
    BaseValidator,
)
from .fields.email import (
    email_validator,
    validate_email,
)
from .fields.file import (
    file_extension_validator,
    file_size_validator,
)
from .fields.name import (
    name_validator,
    validate_name,
)
from .fields.password import (
    password_validator,
    validate_password,
)
from .fields.phone import (
    DEFAULT_PHONE_NUMBER_MESSAGE,
    normalize_phone_number,
    phone_number_validator,
    phone_validator,
    validate_phone_number,
)
from .fields.slug import (
    slug_validator,
    validate_slug,
)
from .fields.url import (
    url_validator,
    validate_url,
)
from .fields.uuid import (
    uuid_validator,
    validate_uuid,
)

__all__: tuple[str, ...] = (
    "BaseValidator",
    "email_validator",
    "validate_email",
    "file_extension_validator",
    "file_size_validator",
    "name_validator",
    "validate_name",
    "password_validator",
    "validate_password",
    "DEFAULT_PHONE_NUMBER_MESSAGE",
    "normalize_phone_number",
    "phone_number_validator",
    "phone_validator",
    "validate_phone_number",
    "slug_validator",
    "validate_slug",
    "url_validator",
    "validate_url",
    "uuid_validator",
    "validate_uuid",
)
