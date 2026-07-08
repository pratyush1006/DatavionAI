"""
Permission classes for laboratory order operations.
"""

from __future__ import annotations

from rest_framework.permissions import IsAuthenticated


class IsLaboratoryOrderUser(
    IsAuthenticated,
):
    """
    Permission for laboratory order operations.

    This currently requires authentication and serves as the
    extension point for future RBAC integration.
    """


__all__ = [
    "IsLaboratoryOrderUser",
]
