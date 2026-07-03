"""
RBAC permission classes.
"""

from .assignment import (
    CanAssignPermission,
    CanAssignRole,
    CanRemovePermission,
    CanRemoveRole,
)
from .base import BaseRBACPermission
from .permission import (
    CanCreatePermission,
    CanDeletePermission,
    CanUpdatePermission,
    CanViewPermission,
)
from .role import (
    CanCreateRole,
    CanDeleteRole,
    CanUpdateRole,
    CanViewRole,
)

__all__ = (
    "BaseRBACPermission",
    "CanAssignRole",
    "CanRemoveRole",
    "CanAssignPermission",
    "CanRemovePermission",
    "CanViewRole",
    "CanCreateRole",
    "CanUpdateRole",
    "CanDeleteRole",
    "CanViewPermission",
    "CanCreatePermission",
    "CanUpdatePermission",
    "CanDeletePermission",
)
