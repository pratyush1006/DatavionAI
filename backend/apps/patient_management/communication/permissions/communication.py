"""RBAC permissions for Patient Communication."""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase


class PatientCommunicationPermission(RBACPermissionBase):
    """Define RBAC permission codes for Patient Communication."""

    VIEW = "patient_communication.view"
    CREATE = "patient_communication.create"
    UPDATE = "patient_communication.update"
    DELETE = "patient_communication.delete"
    RESTORE = "patient_communication.restore"
    QUEUE = "patient_communication.queue"
    SEND = "patient_communication.send"
    DELIVER = "patient_communication.deliver"
    READ = "patient_communication.read"
    FAIL = "patient_communication.fail"
    CANCEL = "patient_communication.cancel"
    ARCHIVE = "patient_communication.archive"


__all__ = ("PatientCommunicationPermission",)
