"""
RBAC constants exports.
"""

from __future__ import annotations

from .organization_role import (
    DEFAULT_ORGANIZATION_ROLE_ASSIGNMENT_SOURCE,
    OrganizationRoleAssignmentSource,
)

# ============================================================================
# Permission
# ============================================================================
from .permission import (
    PermissionAction,
    PermissionModule,
    PermissionScope,
    SystemRole,
)

# ============================================================================
# Permission Group
# ============================================================================
from .permission_group import (
    PermissionGroupCode,
)

# ============================================================================
# Role
# ============================================================================
from .role import (
    DEFAULT_DISPLAY_ORDER,
    DEFAULT_ROLE_CATEGORY,
    DEFAULT_ROLE_PRIORITY,
    DEFAULT_ROLE_SCOPE,
    DEFAULT_ROLE_TYPE,
    RESERVED_ROLE_CODES,
    RESERVED_ROLE_NAMES,
    ROLE_PRIORITIES,
    SYSTEM_ROLE_CODES,
    RoleCategory,
    RoleCode,
    RoleScope,
    RoleType,
)
from .role_hierarchy import (
    DEFAULT_ROLE_HIERARCHY_ASSIGNMENT_SOURCE,
    DEFAULT_ROLE_HIERARCHY_TYPE,
    MAX_ROLE_HIERARCHY_DEPTH,
    RoleHierarchyAssignmentSource,
    RoleHierarchyType,
)

# ============================================================================
# Role Permission
# ============================================================================
from .role_permission import (
    DEFAULT_ROLE_PERMISSION_SOURCE,
    DEFAULT_ROLE_PERMISSION_TYPE,
    RolePermissionSource,
    RolePermissionType,
)

# ============================================================================
# User Role
# ============================================================================
from .user_role import (
    DEFAULT_USER_ROLE_ASSIGNMENT_SOURCE,
    UserRoleAssignmentSource,
)

__all__ = [
    # =========================================================================
    # Permission
    # =========================================================================
    "PermissionAction",
    "PermissionModule",
    "PermissionScope",
    "SystemRole",
    # =========================================================================
    # Permission Group
    # =========================================================================
    "PermissionGroupCode",
    # =========================================================================
    # Role
    # =========================================================================
    "DEFAULT_DISPLAY_ORDER",
    "DEFAULT_ROLE_CATEGORY",
    "DEFAULT_ROLE_PRIORITY",
    "DEFAULT_ROLE_SCOPE",
    "DEFAULT_ROLE_TYPE",
    "RESERVED_ROLE_CODES",
    "RESERVED_ROLE_NAMES",
    "ROLE_PRIORITIES",
    "SYSTEM_ROLE_CODES",
    "RoleCategory",
    "RoleCode",
    "RoleScope",
    "RoleType",
    # =========================================================================
    # Role Permission
    # =========================================================================
    "DEFAULT_ROLE_PERMISSION_SOURCE",
    "DEFAULT_ROLE_PERMISSION_TYPE",
    "RolePermissionSource",
    "RolePermissionType",
    # =========================================================================
    # User Role
    # =========================================================================
    "DEFAULT_USER_ROLE_ASSIGNMENT_SOURCE",
    "UserRoleAssignmentSource",
    "DEFAULT_ORGANIZATION_ROLE_ASSIGNMENT_SOURCE",
    "OrganizationRoleAssignmentSource",
    "DEFAULT_ROLE_HIERARCHY_ASSIGNMENT_SOURCE",
    "DEFAULT_ROLE_HIERARCHY_TYPE",
    "MAX_ROLE_HIERARCHY_DEPTH",
    "RoleHierarchyAssignmentSource",
    "RoleHierarchyType",
]
