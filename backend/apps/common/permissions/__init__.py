"""
Public permission API for the Datavion AI platform.

Feature applications should import reusable permission
classes from this package instead of importing individual
modules directly.
"""

from __future__ import annotations

from .base import (
    BasePermission,
    DatavionPermission,
)

__all__ = [
    "BasePermission",
    "DatavionPermission",
]
