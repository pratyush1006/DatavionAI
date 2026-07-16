"""
Base permission classes.

Provides the foundation for all Datavion AI permission
classes.
"""

from __future__ import annotations

from rest_framework.permissions import BasePermission as DRFBasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.platform.rbac.engines import (
    user_has_permission,
)


class DatavionPermission(
    DRFBasePermission,
):
    """
    Base permission class for Datavion AI.

    Feature-specific permission classes should inherit from
    this class and define a required_permission when
    applicable.
    """

    required_permission: str | None = None

    message = "You do not have permission to perform this action."

    def has_permission(
        self,
        request: Request,
        view: APIView,
    ) -> bool:
        """
        Determine whether the request should be permitted.
        """

        user = request.user

        #
        # Authentication is always required.
        #
        if not user.is_authenticated:
            return False

        #
        # Permission-less endpoints only require authentication.
        #
        if self.required_permission is None:
            return True

        #
        # Resolve organization context.
        #
        organization = getattr(
            request,
            "organization",
            None,
        )

        return user_has_permission(
            user=user,
            permission=self.required_permission,
            organization=organization,
        )

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


#
# Backward compatibility.
#
BasePermission = DatavionPermission


__all__ = [
    "DatavionPermission",
    "BasePermission",
]
