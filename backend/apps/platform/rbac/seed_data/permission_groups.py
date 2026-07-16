"""
Built-in permission groups.
"""

from __future__ import annotations

from apps.platform.rbac.constants import (
    PermissionGroupCode,
)

PERMISSION_GROUPS = [
    {
        "code": group.value,
        "name": group.label,
        "description": (f"{group.label} permission group."),
    }
    for group in PermissionGroupCode
]

__all__ = [
    "PERMISSION_GROUPS",
]
