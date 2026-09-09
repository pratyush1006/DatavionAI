"""
DRF permissions for Patient Addresses.
"""

from apps.platform.rbac.permissions.base import (
    RBACPermissionBase,
)


class CanViewAddress(
    RBACPermissionBase,
):
    permission_code = "addresses.view"


class CanCreateAddress(
    RBACPermissionBase,
):
    permission_code = "addresses.create"


class CanUpdateAddress(
    RBACPermissionBase,
):
    permission_code = "addresses.update"


class CanDeleteAddress(
    RBACPermissionBase,
):
    permission_code = "addresses.delete"


class CanVerifyAddress(
    RBACPermissionBase,
):
    permission_code = "addresses.verify"


class CanActivateAddress(
    RBACPermissionBase,
):
    permission_code = "addresses.activate"


class CanDeactivateAddress(
    RBACPermissionBase,
):
    permission_code = "addresses.deactivate"


class CanSetPrimaryAddress(
    RBACPermissionBase,
):
    permission_code = "addresses.set_primary"


__all__ = (
    "CanActivateAddress",
    "CanCreateAddress",
    "CanDeactivateAddress",
    "CanDeleteAddress",
    "CanSetPrimaryAddress",
    "CanUpdateAddress",
    "CanVerifyAddress",
    "CanViewAddress",
)
