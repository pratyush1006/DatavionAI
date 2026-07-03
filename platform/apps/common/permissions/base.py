"""
Base permission classes.

Provides the foundation for all Datavion AI permission
classes.
"""

from __future__ import annotations

from rest_framework.permissions import BasePermission as DRFBasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class DatavionPermission(DRFBasePermission):
    """
    Base permission class for Datavion AI.

    Feature-specific permission classes should inherit from
    this class and define a permission_code when applicable.
    """

    permission_code: str | None = None

    message = "You do not have permission to perform this action."

    def has_permission(
        self,
        request: Request,
        view: APIView,
    ) -> bool:
        """
        Determine whether the request should be permitted.
        """

        return True

    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        obj: object,
    ) -> bool:
        """
        Determine whether access to a specific object should
        be permitted.
        """

        return self.has_permission(
            request,
            view,
        )


# ------------------------------------------------------------------
# Backward compatibility
# ------------------------------------------------------------------

BasePermission = DatavionPermission


__all__ = [
    "DatavionPermission",
    "BasePermission",
]
