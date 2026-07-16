"""
Common admin exports.

This module exists for backwards compatibility.

Prefer importing from:

    apps.common.admin
"""

from apps.common.admin.base import (
    BaseAdmin,
)

__all__ = [
    "BaseAdmin",
]
