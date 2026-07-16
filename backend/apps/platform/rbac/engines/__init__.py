"""
RBAC authorization engine exports.
"""

from __future__ import annotations

from .permission import (
    get_effective_permissions,
    user_has_permission,
)

__all__ = [
    "get_effective_permissions",
    "user_has_permission",
]
