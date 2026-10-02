"""Canonical Clinical Allergies RBAC adapters."""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase


class CanViewAllergy(RBACPermissionBase):
    permission_code = "allergies.view"
    message = "You do not have permission to view allergies."


class CanCreateAllergy(RBACPermissionBase):
    permission_code = "allergies.create"
    message = "You do not have permission to create allergies."


class CanUpdateAllergy(RBACPermissionBase):
    permission_code = "allergies.update"
    message = "You do not have permission to update allergies."


class CanDeleteAllergy(RBACPermissionBase):
    permission_code = "allergies.delete"
    message = "You do not have permission to delete allergies."


__all__ = (
    "CanViewAllergy",
    "CanCreateAllergy",
    "CanUpdateAllergy",
    "CanDeleteAllergy",
)
