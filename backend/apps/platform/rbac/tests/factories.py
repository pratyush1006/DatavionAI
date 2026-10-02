"""
RBAC test factories.
"""

from .factories.permission import (
    PermissionFactory,
)
from .factories.permission_group import (
    PermissionGroupFactory,
)

__all__ = [
    "PermissionFactory",
    "PermissionGroupFactory",
]
