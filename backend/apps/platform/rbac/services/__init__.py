"""
RBAC service exports.
"""

from __future__ import annotations

from .organization_role import (
    activate_organization_role,
    create_organization_role,
    deactivate_organization_role,
    delete_organization_role,
    update_organization_role,
)

# ============================================================================
# Permission
# ============================================================================
from .permission import (
    create_permission,
    delete_permission,
    restore_permission,
    update_permission,
)

# ============================================================================
# Permission Group
# ============================================================================
from .permission_group import (
    create_permission_group,
    delete_permission_group,
    restore_permission_group,
    update_permission_group,
)

# ============================================================================
# Role
# ============================================================================
from .role import (
    activate_role,
    create_role,
    deactivate_role,
    delete_role,
    make_default_role,
    update_role,
)

# ============================================================================
# Role Hierarchy
# ============================================================================
from .role_hierarchy import (
    activate_role_hierarchy,
    create_role_hierarchy,
    deactivate_role_hierarchy,
    delete_role_hierarchy,
    update_role_hierarchy,
)

# ============================================================================
# Role Permission
# ============================================================================
from .role_permission import (
    activate_role_permission,
    create_role_permission,
    deactivate_role_permission,
    delete_role_permission,
    update_role_permission,
)

# ============================================================================
# User Role
# ============================================================================
from .user_role import (
    activate_user_role,
    create_user_role,
    deactivate_user_role,
    delete_user_role,
    update_user_role,
)

__all__ = [
    # =========================================================================
    # Permission
    # ============================================================================
    "create_permission",
    "delete_permission",
    "restore_permission",
    "update_permission",
    # =========================================================================
    # Permission Group
    # ============================================================================
    "create_permission_group",
    "delete_permission_group",
    "restore_permission_group",
    "update_permission_group",
    # =========================================================================
    # Role
    # ============================================================================
    "activate_role",
    "create_role",
    "deactivate_role",
    "delete_role",
    "make_default_role",
    "update_role",
    # =========================================================================
    # Role Permission
    # ============================================================================
    "activate_role_permission",
    "create_role_permission",
    "deactivate_role_permission",
    "delete_role_permission",
    "update_role_permission",
    # =========================================================================
    # User Role
    # ============================================================================
    "activate_user_role",
    "create_user_role",
    "deactivate_user_role",
    "delete_user_role",
    "update_user_role",
    "activate_organization_role",
    "create_organization_role",
    "deactivate_organization_role",
    "delete_organization_role",
    "update_organization_role",
    # ============================================================================
    # Role Hierarchy
    # ============================================================================
    "activate_role_hierarchy",
    "create_role_hierarchy",
    "deactivate_role_hierarchy",
    "delete_role_hierarchy",
    "update_role_hierarchy",
]
