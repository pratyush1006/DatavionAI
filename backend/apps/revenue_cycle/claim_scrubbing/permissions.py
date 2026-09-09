"""RBAC permissions for claim scrubbing."""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase


class ClaimScrubbingPermission(RBACPermissionBase):
    """Enforce claim scrubbing RBAC permissions."""

    permission = "revenue_cycle.claim_scrubbing.manage"


class ClaimScrubbingViewPermission(RBACPermissionBase):
    """Enforce read access to claim scrubbing."""

    permission = "revenue_cycle.claim_scrubbing.view"


__all__ = ("ClaimScrubbingPermission", "ClaimScrubbingViewPermission")
