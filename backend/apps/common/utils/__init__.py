"""
Public utility API for the Datavion AI platform.

Feature applications should import reusable framework
utilities from this package instead of importing
individual utility modules directly.
"""

from __future__ import annotations

from .codes import (
    ALPHANUMERIC_CHARACTERS as CODE_CHARACTERS,
)
from .codes import (
    DEFAULT_CODE_LENGTH,
    generate_random_code,
)
from .security import (
    ALPHANUMERIC_CHARACTERS as RANDOM_STRING_CHARACTERS,
)
from .security import (
    DEFAULT_RANDOM_STRING_LENGTH,
    generate_random_string,
)
from .strings import (
    mask_email,
    mask_phone_number,
    normalize_whitespace,
    truncate,
)

__all__ = [
    "DEFAULT_CODE_LENGTH",
    "DEFAULT_RANDOM_STRING_LENGTH",
    "CODE_CHARACTERS",
    "RANDOM_STRING_CHARACTERS",
    "generate_random_code",
    "generate_random_string",
    "mask_email",
    "mask_phone_number",
    "normalize_whitespace",
    "truncate",
]
