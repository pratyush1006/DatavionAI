"""
RBAC permissions for Patient Timeline.

Permission classes are evaluated by the platform RBAC base class.
"""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase


class CanViewTimeline(RBACPermissionBase):
    """Authorize viewing a Timeline entry."""

    permission_code = "patient_timeline.view"
    message = "You do not have permission to view patient timeline."


class CanListTimeline(RBACPermissionBase):
    """Authorize listing Timeline entries."""

    permission_code = "patient_timeline.list"
    message = "You do not have permission to list patient timeline."


class CanCreateTimeline(RBACPermissionBase):
    """Authorize creating Timeline entries."""

    permission_code = "patient_timeline.create"
    message = "You do not have permission to create patient timeline entries."


class CanUpdateTimeline(RBACPermissionBase):
    """Authorize updating Timeline entries."""

    permission_code = "patient_timeline.update"
    message = "You do not have permission to update patient timeline entries."


class CanRestoreTimeline(RBACPermissionBase):
    """Authorize restoring deleted Timeline entries."""

    permission_code = "patient_timeline.restore"
    message = "You do not have permission to restore patient timeline entries."


class CanDeleteTimeline(RBACPermissionBase):
    """Authorize deleting Timeline entries."""

    permission_code = "patient_timeline.delete"
    message = "You do not have permission to delete patient timeline entries."


class CanActivateTimeline(RBACPermissionBase):
    """Authorize activating Timeline entries."""

    permission_code = "patient_timeline.activate"
    message = "You do not have permission to activate patient timeline entries."


class CanDeactivateTimeline(RBACPermissionBase):
    """Authorize deactivating Timeline entries."""

    permission_code = "patient_timeline.deactivate"
    message = "You do not have permission to deactivate patient timeline entries."


class CanArchiveTimeline(RBACPermissionBase):
    """Authorize archiving Timeline entries."""

    permission_code = "patient_timeline.archive"
    message = "You do not have permission to archive patient timeline entries."


__all__ = (
    "CanActivateTimeline",
    "CanArchiveTimeline",
    "CanCreateTimeline",
    "CanDeactivateTimeline",
    "CanDeleteTimeline",
    "CanListTimeline",
    "CanRestoreTimeline",
    "CanUpdateTimeline",
    "CanViewTimeline",
)
