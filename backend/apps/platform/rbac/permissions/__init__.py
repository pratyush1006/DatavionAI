"""
RBAC permission exports.

Central export registry for DatavionOS
authorization permission classes.
"""

from __future__ import annotations

# ============================================================================
# Assignment
# ============================================================================
from .assignment import (
    CanAssignPermission,
    CanAssignRole,
    CanRemovePermission,
    CanRemoveRole,
)

# ============================================================================
# Base
# ============================================================================
from .base import (
    RBACPermissionBase,
)

# ============================================================================
# Organization Role
# ============================================================================
from .organization_role import (
    CanCreateOrganizationRole,
    CanDeleteOrganizationRole,
    CanUpdateOrganizationRole,
    CanViewOrganizationRole,
)

# ============================================================================
# Permission
# ============================================================================
from .permission import (
    CanCreatePermission,
    CanDeletePermission,
    CanUpdatePermission,
    CanViewPermission,
)

# ============================================================================
# Permission Group
# ============================================================================
from .permission_group import (
    CanCreatePermissionGroup,
    CanDeletePermissionGroup,
    CanUpdatePermissionGroup,
    CanViewPermissionGroup,
)

# ============================================================================
# Role
# ============================================================================
from .role import (
    CanCreateRole,
    CanDeleteRole,
    CanUpdateRole,
    CanViewRole,
)

# ============================================================================
# Role Hierarchy
# ============================================================================
from .role_hierarchy import (
    CanCreateRoleHierarchy,
    CanDeleteRoleHierarchy,
    CanUpdateRoleHierarchy,
    CanViewRoleHierarchy,
)

# ============================================================================
# Role Permission
# ============================================================================
from .role_permission import (
    CanCreateRolePermission,
    CanDeleteRolePermission,
    CanUpdateRolePermission,
    CanViewRolePermission,
)

# ============================================================================
# User Role
# ============================================================================
from .user_role import (
    CanCreateUserRole,
    CanDeleteUserRole,
    CanUpdateUserRole,
    CanViewUserRole,
)

__all__ = [
    # =========================================================================
    # Base
    # =========================================================================
    "RBACPermissionBase",
    # =========================================================================
    # Assignment
    # =========================================================================
    "CanAssignPermission",
    "CanAssignRole",
    "CanRemovePermission",
    "CanRemoveRole",
    # =========================================================================
    # Organization Role
    # =========================================================================
    "CanCreateOrganizationRole",
    "CanDeleteOrganizationRole",
    "CanUpdateOrganizationRole",
    "CanViewOrganizationRole",
    # =========================================================================
    # Permission
    # =========================================================================
    "CanCreatePermission",
    "CanDeletePermission",
    "CanUpdatePermission",
    "CanViewPermission",
    # =========================================================================
    # Permission Group
    # =========================================================================
    "CanCreatePermissionGroup",
    "CanDeletePermissionGroup",
    "CanUpdatePermissionGroup",
    "CanViewPermissionGroup",
    # =========================================================================
    # Role
    # =========================================================================
    "CanCreateRole",
    "CanDeleteRole",
    "CanUpdateRole",
    "CanViewRole",
    # =========================================================================
    # Role Permission
    # =========================================================================
    "CanCreateRolePermission",
    "CanDeleteRolePermission",
    "CanUpdateRolePermission",
    "CanViewRolePermission",
    # =========================================================================
    # User Role
    # =========================================================================
    "CanCreateUserRole",
    "CanDeleteUserRole",
    "CanUpdateUserRole",
    "CanViewUserRole",
    # =========================================================================
    # Role Hierarchy
    # =========================================================================
    "CanCreateRoleHierarchy",
    "CanDeleteRoleHierarchy",
    "CanUpdateRoleHierarchy",
    "CanViewRoleHierarchy",
]
