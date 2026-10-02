"""Canonical Vitals RBAC adapters."""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase


class CanViewVital(RBACPermissionBase):
    permission_code = "vitals.view"
    message = "You do not have permission to view vitals."


class CanCreateVital(RBACPermissionBase):
    permission_code = "vitals.create"
    message = "You do not have permission to create vitals."


class CanUpdateVital(RBACPermissionBase):
    permission_code = "vitals.update"
    message = "You do not have permission to update vitals."


class CanDeleteVital(RBACPermissionBase):
    permission_code = "vitals.delete"
    message = "You do not have permission to delete vitals."


__all__ = (
    "CanViewVital",
    "CanCreateVital",
    "CanUpdateVital",
    "CanDeleteVital",
)
