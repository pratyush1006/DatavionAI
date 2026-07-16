"""
Permission classes for laboratory test operations.
"""

from __future__ import annotations

from rest_framework.permissions import IsAuthenticated


class IsLaboratoryTestUser(
    IsAuthenticated,
):
    """
    Permission for laboratory test operations.

    This currently requires authentication and serves as the
    extension point for future RBAC integration.
    """


__all__ = [
    "IsLaboratoryTestUser",
]
