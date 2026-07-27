"""
Base permission classes.

Provides framework-level permission primitives for DatavionOS.

Framework permissions must remain independent of feature modules
such as RBAC, Organizations, Patients, or Laboratories.
"""

from __future__ import annotations

from abc import abstractmethod

from rest_framework.permissions import BasePermission as DRFBasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class DatavionPermission(
    DRFBasePermission,
):
    """
    Base permission class.

    Subclasses may specify a ``required_permission`` and implement
    ``check_permission()`` to integrate with an authorization engine
    such as RBAC.

    This class intentionally contains no knowledge of how permissions
    are resolved.
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

        if not user.is_authenticated:
            return False

        if self.required_permission is None:
            return True

        return self.check_permission(
            request=request,
            permission=self.required_permission,
        )

    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        obj: object,
    ) -> bool:
        """
        Determine whether access to an object should be permitted.
        """

        return self.has_permission(
            request=request,
            view=view,
        )

    @abstractmethod
    def check_permission(
        self,
        request: Request,
        permission: str,
    ) -> bool:
        """
        Determine whether the authenticated user has the specified
        permission.

        Subclasses must provide the authorization implementation.
        """
        raise NotImplementedError


BasePermission = DatavionPermission


__all__ = (
    "BasePermission",
    "DatavionPermission",
)
