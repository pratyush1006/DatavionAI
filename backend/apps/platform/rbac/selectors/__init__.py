"""
RBAC selector exports.
"""

from __future__ import annotations

from .organization_role import (
    get_active_organization_roles,
    get_inactive_organization_roles,
    get_organization_role_by_id,
    get_organization_roles,
    get_organization_roles_for_organization,
    get_organization_roles_for_role,
    get_organization_roles_for_user,
    get_primary_organization_roles,
    search_organization_roles,
)

# ============================================================================
# Permission
# ============================================================================
from .permission import (
    get_assignable_permissions,
    get_custom_permissions,
    get_delegable_permissions,
    get_inactive_permissions,
    get_permission_by_code,
    get_permission_by_id,
    get_permissions,
    get_permissions_by_action,
    get_permissions_by_module,
    get_permissions_by_scope,
    get_system_permissions,
    search_permissions,
)

# ============================================================================
# Permission Group
# ============================================================================
from .permission_group import (
    get_custom_permission_groups,
    get_inactive_permission_groups,
    get_permission_group_by_code,
    get_permission_group_by_id,
    get_permission_groups,
    get_permission_groups_by_module,
    get_system_permission_groups,
    search_permission_groups,
)

# ============================================================================
# Role
# ============================================================================
from .role import (
    get_active_roles,
    get_assignable_roles,
    get_custom_roles,
    get_default_roles,
    get_inactive_roles,
    get_role_by_code,
    get_role_by_id,
    get_roles,
    get_roles_by_category,
    get_roles_by_scope,
    get_roles_by_type,
    get_system_roles,
    search_roles,
)
from .role_hierarchy import (
    get_active_role_hierarchies,
    get_child_role_hierarchies,
    get_direct_role_hierarchies,
    get_inactive_role_hierarchies,
    get_inherited_role_hierarchies,
    get_parent_role_hierarchies,
    get_role_hierarchies,
    get_role_hierarchy_by_id,
    search_role_hierarchies,
)

# ============================================================================
# Role Permission
# ============================================================================
from .role_permission import (
    get_direct_role_permissions,
    get_inherited_role_permissions,
    get_role_permission_by_id,
    get_role_permissions,
    get_role_permissions_for_permission,
    get_role_permissions_for_role,
    search_role_permissions,
)

# ============================================================================
# User Role
# ============================================================================
from .user_role import (
    get_user_role_by_id,
    get_user_roles,
    get_user_roles_for_role,
    get_user_roles_for_user,
    search_user_roles,
)

__all__ = [
    # =========================================================================
    # Permission
    # =========================================================================
    "get_assignable_permissions",
    "get_custom_permissions",
    "get_delegable_permissions",
    "get_inactive_permissions",
    "get_permission_by_code",
    "get_permission_by_id",
    "get_permissions",
    "get_permissions_by_action",
    "get_permissions_by_module",
    "get_permissions_by_scope",
    "get_system_permissions",
    "search_permissions",
    # =========================================================================
    # Permission Group
    # =========================================================================
    "get_custom_permission_groups",
    "get_inactive_permission_groups",
    "get_permission_group_by_code",
    "get_permission_group_by_id",
    "get_permission_groups",
    "get_permission_groups_by_module",
    "get_system_permission_groups",
    "search_permission_groups",
    # =========================================================================
    # Role
    # =========================================================================
    "get_active_roles",
    "get_assignable_roles",
    "get_custom_roles",
    "get_default_roles",
    "get_inactive_roles",
    "get_role_by_code",
    "get_role_by_id",
    "get_roles",
    "get_roles_by_category",
    "get_roles_by_scope",
    "get_roles_by_type",
    "get_system_roles",
    "search_roles",
    # =========================================================================
    # Role Permission
    # =========================================================================
    "get_direct_role_permissions",
    "get_inherited_role_permissions",
    "get_role_permission_by_id",
    "get_role_permissions",
    "get_role_permissions_for_permission",
    "get_role_permissions_for_role",
    "search_role_permissions",
    # =========================================================================
    # User Role
    # =========================================================================
    "get_user_role_by_id",
    "get_user_roles",
    "get_user_roles_for_role",
    "get_user_roles_for_user",
    "search_user_roles",
    "get_active_organization_roles",
    "get_inactive_organization_roles",
    "get_organization_role_by_id",
    "get_organization_roles",
    "get_organization_roles_for_organization",
    "get_organization_roles_for_role",
    "get_organization_roles_for_user",
    "get_primary_organization_roles",
    "search_organization_roles",
    "get_active_role_hierarchies",
    "get_child_role_hierarchies",
    "get_direct_role_hierarchies",
    "get_inactive_role_hierarchies",
    "get_inherited_role_hierarchies",
    "get_parent_role_hierarchies",
    "get_role_hierarchies",
    "get_role_hierarchy_by_id",
    "search_role_hierarchies",
]
