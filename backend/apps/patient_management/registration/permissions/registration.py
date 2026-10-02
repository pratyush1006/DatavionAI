"""
DRF permissions for Patient Registration.

HTTP permission classes are deliberately thin. They delegate authorization
to the platform RBAC engine through the shared RBAC permission base.
"""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase


class CanViewRegistration(RBACPermissionBase):
    """Allow users with registration view permission."""

    permission_code = "registrations.view"


class CanCreateRegistration(RBACPermissionBase):
    """Allow users with registration create permission."""

    permission_code = "registrations.create"


class CanUpdateRegistration(RBACPermissionBase):
    """Allow users with registration update permission."""

    permission_code = "registrations.update"


class CanVerifyRegistration(RBACPermissionBase):
    """Allow users with registration verification permission."""

    permission_code = "registrations.verify"


class CanCheckInRegistration(RBACPermissionBase):
    """Allow users with registration check-in permission."""

    permission_code = "registrations.check_in"


class CanCompleteRegistration(RBACPermissionBase):
    """Allow users with registration completion permission."""

    permission_code = "registrations.complete"


class CanCancelRegistration(RBACPermissionBase):
    """Allow users with registration cancellation permission."""

    permission_code = "registrations.cancel"


class CanRejectRegistration(RBACPermissionBase):
    """Allow users with registration rejection permission."""

    permission_code = "registrations.reject"


class CanNoShowRegistration(RBACPermissionBase):
    """Allow users with registration no-show permission."""

    permission_code = "registrations.no_show"


class CanDeleteRegistration(RBACPermissionBase):
    """Allow users with registration deletion permission."""

    permission_code = "registrations.delete"


__all__ = (
    "CanCancelRegistration",
    "CanCheckInRegistration",
    "CanCompleteRegistration",
    "CanCreateRegistration",
    "CanDeleteRegistration",
    "CanNoShowRegistration",
    "CanRejectRegistration",
    "CanUpdateRegistration",
    "CanVerifyRegistration",
    "CanViewRegistration",
)
