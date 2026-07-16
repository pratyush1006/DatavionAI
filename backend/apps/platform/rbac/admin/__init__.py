"""
RBAC admin registrations.
"""

from __future__ import annotations

# ============================================================================
# Permission
# ============================================================================
from .permission import (
    PermissionAdmin,
)

# ============================================================================
# Permission Group
# ============================================================================
from .permission_group import (
    PermissionGroupAdmin,
)

# ============================================================================
# Role
# ============================================================================
from .role import (
    RoleAdmin,
)

# ============================================================================
# Role Permission
# ============================================================================
from .role_permission import (
    RolePermissionAdmin,
)

__all__ = [
    "PermissionAdmin",
    "PermissionGroupAdmin",
    "RoleAdmin",
    "RolePermissionAdmin",
]
