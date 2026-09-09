"""
DRF permissions for Patient Contacts.

These permission classes are intentionally thin adapters around the
platform RBAC permission infrastructure.

Authorization logic remains in the ContactPolicy layer and the
platform RBAC engine.
"""

from __future__ import annotations

from apps.platform.rbac.permissions import RBACPermissionBase


class CanViewContact(RBACPermissionBase):
    """Permission to view patient contacts."""

    permission_code = "contacts.view"


class CanCreateContact(RBACPermissionBase):
    """Permission to create patient contacts."""

    permission_code = "contacts.create"


class CanUpdateContact(RBACPermissionBase):
    """Permission to update patient contacts."""

    permission_code = "contacts.update"


class CanDeleteContact(RBACPermissionBase):
    """Permission to delete patient contacts."""

    permission_code = "contacts.delete"


class CanVerifyContact(RBACPermissionBase):
    """Permission to verify patient contacts."""

    permission_code = "contacts.verify"


class CanActivateContact(RBACPermissionBase):
    """Permission to activate patient contacts."""

    permission_code = "contacts.activate"


class CanDeactivateContact(RBACPermissionBase):
    """Permission to deactivate patient contacts."""

    permission_code = "contacts.deactivate"


class CanSetPrimaryContact(RBACPermissionBase):
    """Permission to set a patient contact as primary."""

    permission_code = "contacts.set_primary"


__all__ = (
    "CanActivateContact",
    "CanCreateContact",
    "CanDeactivateContact",
    "CanDeleteContact",
    "CanSetPrimaryContact",
    "CanUpdateContact",
    "CanVerifyContact",
    "CanViewContact",
)
