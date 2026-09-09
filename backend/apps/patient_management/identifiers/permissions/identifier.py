"""
DRF permissions for Patient Identifiers.

HTTP permission classes are deliberately thin. They delegate authorization
to the platform RBAC engine through the shared RBAC permission base.
"""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase


class CanViewIdentifier(RBACPermissionBase):
    """Allow users with identifier view permission."""

    permission_code = "identifiers.view"


class CanCreateIdentifier(RBACPermissionBase):
    """Allow users with identifier create permission."""

    permission_code = "identifiers.create"


class CanUpdateIdentifier(RBACPermissionBase):
    """Allow users with identifier update permission."""

    permission_code = "identifiers.update"


class CanVerifyIdentifier(RBACPermissionBase):
    """Allow users with identifier verification permission."""

    permission_code = "identifiers.verify"


class CanActivateIdentifier(RBACPermissionBase):
    """Allow users with identifier activation permission."""

    permission_code = "identifiers.activate"


class CanDeactivateIdentifier(RBACPermissionBase):
    """Allow users with identifier deactivation permission."""

    permission_code = "identifiers.deactivate"


class CanRevokeIdentifier(RBACPermissionBase):
    """Allow users with identifier revocation permission."""

    permission_code = "identifiers.revoke"


class CanSetPrimaryIdentifier(RBACPermissionBase):
    """Allow users with identifier primary-status permission."""

    permission_code = "identifiers.set_primary"


class CanDeleteIdentifier(RBACPermissionBase):
    """Allow users with identifier deletion permission."""

    permission_code = "identifiers.delete"


__all__ = (
    "CanActivateIdentifier",
    "CanCreateIdentifier",
    "CanDeactivateIdentifier",
    "CanDeleteIdentifier",
    "CanRevokeIdentifier",
    "CanSetPrimaryIdentifier",
    "CanUpdateIdentifier",
    "CanVerifyIdentifier",
    "CanViewIdentifier",
)
