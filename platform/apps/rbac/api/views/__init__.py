"""
RBAC API views.
"""

from .permission import (
    PermissionListCreateAPIView,
    PermissionRetrieveUpdateDestroyAPIView,
)
from .role import (
    RoleListCreateAPIView,
    RoleRetrieveUpdateDestroyAPIView,
)

__all__ = [
    "RoleListCreateAPIView",
    "RoleRetrieveUpdateDestroyAPIView",
    "PermissionListCreateAPIView",
    "PermissionRetrieveUpdateDestroyAPIView",
]
