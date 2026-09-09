"""
Revenue Cycle Appeals RBAC permission exports.
"""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase


class AppealReadPermission(RBACPermissionBase):
    """Authorize read access to appeals."""

    permission_code = "revenue_cycle.appeals.read"


class AppealManagePermission(RBACPermissionBase):
    """Authorize mutation access to appeals."""

    permission_code = "revenue_cycle.appeals.manage"


__all__ = (
    "AppealManagePermission",
    "AppealReadPermission",
)
