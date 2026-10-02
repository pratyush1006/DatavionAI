"""
Framework permission utilities.

Provides reusable permission classes and mixins for DatavionOS.

Business-specific authorization belongs in feature modules such as
RBAC and should extend these framework primitives.
"""

from __future__ import annotations

from .authentication import (
    AllowAny,
    DenyAll,
    IsAuthenticated,
    IsAuthenticatedAndActive,
    IsAuthenticatedOrReadOnly,
)
from .base import (
    BasePermission,
    DatavionPermission,
)
from .mixins import (
    MultiplePermissionsMixin,
    PermissionAPIView,
    PermissionRequiredMixin,
)

__all__ = (
    "AllowAny",
    "BasePermission",
    "DatavionPermission",
    "DenyAll",
    "IsAuthenticated",
    "IsAuthenticatedAndActive",
    "IsAuthenticatedOrReadOnly",
    "MultiplePermissionsMixin",
    "PermissionAPIView",
    "PermissionRequiredMixin",
)
