"""
Permission classes for laboratory result operations.
"""

from __future__ import annotations

from rest_framework.permissions import IsAuthenticated


class IsLaboratoryResultUser(
    IsAuthenticated,
):
    """
    Permission for laboratory result operations.

    This currently requires authentication and serves as the
    extension point for future RBAC integration.
    """


__all__ = [
    "IsLaboratoryResultUser",
]
