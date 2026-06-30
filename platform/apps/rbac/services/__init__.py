"""
RBAC write services.
"""

from .permission import (
    create_permission,
    delete_permission,
    update_permission,
)
from .role import (
    create_role,
    delete_role,
    update_role,
)
from .role_permission import (
    assign_permission_to_role,
    remove_permission_from_role,
)
from .user_role import (
    assign_role_to_user,
    remove_role_from_user,
)

__all__ = [
    # Role
    "create_role",
    "update_role",
    "delete_role",
    # Permission
    "create_permission",
    "update_permission",
    "delete_permission",
    # User Role
    "assign_role_to_user",
    "remove_role_from_user",
    # Role Permission
    "assign_permission_to_role",
    "remove_permission_from_role",
]
