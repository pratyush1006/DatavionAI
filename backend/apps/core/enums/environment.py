"""
Environment enumerations for the Datavion AI platform.
"""

from __future__ import annotations

from enum import StrEnum


class Environment(StrEnum):
    """
    Supported deployment environments.
    """

    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


__all__ = [
    "Environment",
]
