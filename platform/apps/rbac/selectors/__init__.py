"""
RBAC selectors.
"""

from .permission import (
    get_permission_by_code,
    get_permission_by_id,
    get_permissions,
)
from .role import (
    get_role_by_code,
    get_role_by_id,
    get_roles,
)
from .role_permission import (
    get_permissions_for_role,
    get_role_permission_by_id,
    get_role_permissions,
    get_roles_for_permission,
)
from .user_role import (
    get_roles_for_user,
    get_user_role_by_id,
    get_user_roles,
    get_users_for_role,
)

__all__ = [
    "get_roles",
    "get_role_by_id",
    "get_role_by_code",
    "get_permissions",
    "get_permission_by_id",
    "get_permission_by_code",
    "get_user_roles",
    "get_user_role_by_id",
    "get_roles_for_user",
    "get_users_for_role",
    "get_role_permissions",
    "get_role_permission_by_id",
    "get_permissions_for_role",
    "get_roles_for_permission",
]
