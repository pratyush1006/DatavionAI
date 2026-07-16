"""
RBAC validator exports.
"""

from __future__ import annotations

from .organization_role import (
    validate_organization_role,
    validate_organization_role_unique,
    validate_primary_organization_role,
)

# ============================================================================
# Permission
# ============================================================================
from .permission import (
    validate_permission,
    validate_permission_action,
    validate_permission_code,
    validate_permission_code_unique,
    validate_permission_module,
    validate_permission_scope,
    validate_permission_unique,
    validate_unique_permission,
)

# ============================================================================
# Permission Group
# ============================================================================
from .permission_group import (
    validate_permission_group,
    validate_permission_group_code_unique,
    validate_permission_group_module,
    validate_permission_group_name_unique,
)

# ============================================================================
# Role
# ============================================================================
from .role import (
    validate_parent_role,
    validate_reserved_role_code,
    validate_reserved_role_name,
    validate_role,
    validate_role_category,
    validate_role_code,
    validate_role_code_unique,
    validate_role_name,
    validate_role_name_unique,
    validate_role_priority,
    validate_role_scope,
    validate_role_type,
    validate_system_role_priority,
)
from .role_hierarchy import (
    validate_role_hierarchy,
    validate_role_hierarchy_cycle,
    validate_role_hierarchy_unique,
    validate_self_role_hierarchy,
)

# ============================================================================
# Role Permission
# ============================================================================
from .role_permission import (
    validate_role_permission,
    validate_role_permission_source,
    validate_role_permission_type,
    validate_role_permission_unique,
    validate_system_role_permission,
)

# ============================================================================
# User Role
# ============================================================================
from .user_role import (
    validate_unique_user_role,
    validate_user_role,
)

__all__ = [
    # =========================================================================
    # Permission
    # ============================================================================
    "validate_permission",
    "validate_permission_action",
    "validate_permission_code",
    "validate_permission_code_unique",
    "validate_permission_module",
    "validate_permission_scope",
    "validate_permission_unique",
    "validate_unique_permission",
    # =========================================================================
    # Permission Group
    # ============================================================================
    "validate_permission_group",
    "validate_permission_group_code_unique",
    "validate_permission_group_module",
    "validate_permission_group_name_unique",
    # =========================================================================
    # Role
    # ============================================================================
    "validate_parent_role",
    "validate_reserved_role_code",
    "validate_reserved_role_name",
    "validate_role",
    "validate_role_category",
    "validate_role_code",
    "validate_role_code_unique",
    "validate_role_name",
    "validate_role_name_unique",
    "validate_role_priority",
    "validate_role_scope",
    "validate_role_type",
    "validate_system_role_priority",
    # =========================================================================
    # Role Permission
    # ============================================================================
    "validate_role_permission",
    "validate_role_permission_source",
    "validate_role_permission_type",
    "validate_role_permission_unique",
    "validate_system_role_permission",
    # =========================================================================
    # User Role
    # ============================================================================
    "validate_unique_user_role",
    "validate_user_role",
    "validate_organization_role",
    "validate_organization_role_unique",
    "validate_primary_organization_role",
    "validate_role_hierarchy",
    "validate_role_hierarchy_cycle",
    "validate_role_hierarchy_unique",
    "validate_self_role_hierarchy",
]
