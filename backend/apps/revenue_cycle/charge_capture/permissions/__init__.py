"""RBAC permission definitions for Charge Capture."""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase

__all__ = (
    "ChargeCaptureCreatePermission",
    "ChargeCaptureReadPermission",
    "ChargeCaptureUpdatePermission",
    "ChargeCaptureVoidPermission",
)


class ChargeCaptureCreatePermission(RBACPermissionBase):
    """Authorize creation of charges."""

    codename = "revenue_cycle.charge_capture.create"
    description = "Create revenue-cycle charges."


class ChargeCaptureReadPermission(RBACPermissionBase):
    """Authorize reading charges."""

    codename = "revenue_cycle.charge_capture.read"
    description = "Read revenue-cycle charges."


class ChargeCaptureUpdatePermission(RBACPermissionBase):
    """Authorize lifecycle updates to charges."""

    codename = "revenue_cycle.charge_capture.update"
    description = "Update revenue-cycle charges."


class ChargeCaptureVoidPermission(RBACPermissionBase):
    """Authorize voiding charges."""

    codename = "revenue_cycle.charge_capture.void"
    description = "Void revenue-cycle charges."
