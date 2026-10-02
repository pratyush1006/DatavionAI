"""
RBAC permissions for the Patient Family Members module.

These classes are thin adapters over the centralized DatavionOS
RBAC permission engine.
"""

from __future__ import annotations

from apps.platform.rbac.permissions import RBACPermissionBase


class FamilyMemberPermission:
    """Stable permission codes used by RBAC seeders and integrations."""

    CREATE = "patient_management.family_members.create"
    UPDATE = "patient_management.family_members.update"
    DELETE = "patient_management.family_members.delete"
    VIEW = "patient_management.family_members.view"


class CanViewFamilyMember(RBACPermissionBase):
    permission_code = "family_members.view"
    message = "You do not have permission to view patient family members."


class CanCreateFamilyMember(RBACPermissionBase):
    permission_code = "family_members.create"
    message = "You do not have permission to create patient family members."


class CanUpdateFamilyMember(RBACPermissionBase):
    permission_code = "family_members.update"
    message = "You do not have permission to update patient family members."


class CanDeleteFamilyMember(RBACPermissionBase):
    permission_code = "family_members.delete"
    message = "You do not have permission to delete patient family members."


class CanRestoreFamilyMember(RBACPermissionBase):
    permission_code = "family_members.restore"
    message = "You do not have permission to restore patient family members."


class CanViewSensitiveFamilyMember(RBACPermissionBase):
    permission_code = "family_members.view_sensitive"
    message = "You do not have permission to view sensitive family-member information."


class CanManageNextOfKinFamilyMember(RBACPermissionBase):
    permission_code = "family_members.manage_next_of_kin"
    message = (
        "You do not have permission to manage family-member next-of-kin designations."
    )


class CanManageEmergencyContactFamilyMember(RBACPermissionBase):
    permission_code = "family_members.manage_emergency_contact"
    message = (
        "You do not have permission to manage family-member "
        "emergency-contact designations."
    )


class CanExportFamilyMembers(RBACPermissionBase):
    permission_code = "family_members.export"
    message = "You do not have permission to export family-member data."


class CanImportFamilyMembers(RBACPermissionBase):
    permission_code = "family_members.import"
    message = "You do not have permission to import family-member data."


__all__ = (
    "FamilyMemberPermission",
    "CanViewFamilyMember",
    "CanCreateFamilyMember",
    "CanUpdateFamilyMember",
    "CanDeleteFamilyMember",
    "CanRestoreFamilyMember",
    "CanViewSensitiveFamilyMember",
    "CanManageNextOfKinFamilyMember",
    "CanManageEmergencyContactFamilyMember",
    "CanExportFamilyMembers",
    "CanImportFamilyMembers",
)
