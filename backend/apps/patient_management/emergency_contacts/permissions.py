"""
RBAC permissions for Emergency Contacts.
"""

from __future__ import annotations

from apps.platform.rbac.permissions import RBACPermissionBase


class CanViewEmergencyContact(
    RBACPermissionBase,
):
    """Permission to view emergency contacts."""

    permission_code = "emergency_contacts.view"


class CanCreateEmergencyContact(
    RBACPermissionBase,
):
    """Permission to create emergency contacts."""

    permission_code = "emergency_contacts.create"


class CanUpdateEmergencyContact(
    RBACPermissionBase,
):
    """Permission to update emergency contacts."""

    permission_code = "emergency_contacts.update"


class CanDeleteEmergencyContact(
    RBACPermissionBase,
):
    """Permission to delete emergency contacts."""

    permission_code = "emergency_contacts.delete"


class CanVerifyEmergencyContact(
    RBACPermissionBase,
):
    """Permission to verify emergency contacts."""

    permission_code = "emergency_contacts.verify"


class CanActivateEmergencyContact(
    RBACPermissionBase,
):
    """Permission to activate emergency contacts."""

    permission_code = "emergency_contacts.activate"


class CanDeactivateEmergencyContact(
    RBACPermissionBase,
):
    """Permission to deactivate emergency contacts."""

    permission_code = "emergency_contacts.deactivate"


class CanBlockEmergencyContact(
    RBACPermissionBase,
):
    """Permission to block emergency contacts."""

    permission_code = "emergency_contacts.block"


class CanSetPrimaryEmergencyContact(
    RBACPermissionBase,
):
    """Permission to set the primary emergency contact."""

    permission_code = "emergency_contacts.set_primary"


__all__ = [
    "CanActivateEmergencyContact",
    "CanBlockEmergencyContact",
    "CanCreateEmergencyContact",
    "CanDeactivateEmergencyContact",
    "CanDeleteEmergencyContact",
    "CanSetPrimaryEmergencyContact",
    "CanUpdateEmergencyContact",
    "CanVerifyEmergencyContact",
    "CanViewEmergencyContact",
]
