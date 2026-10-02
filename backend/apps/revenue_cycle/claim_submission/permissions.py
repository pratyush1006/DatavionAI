"""RBAC permissions for claim submission."""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase


class ClaimSubmissionViewPermission(RBACPermissionBase):
    """Authorize claim submission reads."""

    permission_code = "revenue_cycle.claim_submission.view"


class ClaimSubmissionManagePermission(RBACPermissionBase):
    """Authorize claim submission mutations."""

    permission_code = "revenue_cycle.claim_submission.manage"


__all__ = ("ClaimSubmissionViewPermission", "ClaimSubmissionManagePermission")
