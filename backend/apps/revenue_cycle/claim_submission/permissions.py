"""RBAC permissions for claim submission."""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase


class ClaimSubmissionViewPermission(RBACPermissionBase):
    """Authorize claim submission reads."""

    required_permission = "revenue_cycle.claim_submission.view"


class ClaimSubmissionManagePermission(RBACPermissionBase):
    """Authorize claim submission mutations."""

    required_permission = "revenue_cycle.claim_submission.manage"


__all__ = ("ClaimSubmissionViewPermission", "ClaimSubmissionManagePermission")
