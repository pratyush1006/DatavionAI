"""
Constants for the Accounts app.
"""

from __future__ import annotations

# ---------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------

DEFAULT_LANGUAGE = "en"

DEFAULT_TIMEZONE = "UTC"


# ---------------------------------------------------------------------
# Profile
# ---------------------------------------------------------------------

MAX_PHONE_LENGTH = 20

MAX_LANGUAGE_LENGTH = 20

MAX_TIMEZONE_LENGTH = 100


__all__ = [
    "DEFAULT_LANGUAGE",
    "DEFAULT_TIMEZONE",
    "MAX_LANGUAGE_LENGTH",
    "MAX_PHONE_LENGTH",
    "MAX_TIMEZONE_LENGTH",
]
