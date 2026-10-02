"""RBAC permission identifiers and API adapters for Patient Documents."""

from __future__ import annotations

from apps.platform.rbac.permissions.base import (
    RBACPermissionBase,
)


class PatientDocumentPermission:
    """Stable permission codes for the bounded context."""

    LIST = "patient_document.list"
    VIEW = "patient_document.view"
    CREATE = "patient_document.create"
    UPDATE = "patient_document.update"
    ACTIVATE = "patient_document.activate"
    DELETE = "patient_document.delete"
    RESTORE = "patient_document.restore"
    ARCHIVE = "patient_document.archive"
    VERSION_CREATE = "patient_document.version_create"
    ACCESS_AUDIT = "patient_document.access_audit"


class CanListPatientDocuments(RBACPermissionBase):
    """Allow listing patient documents."""

    permission_code = PatientDocumentPermission.LIST
    message = "You do not have permission to list patient documents."


class CanViewPatientDocument(RBACPermissionBase):
    """Allow viewing patient documents."""

    permission_code = PatientDocumentPermission.VIEW
    message = "You do not have permission to view patient documents."


class CanCreatePatientDocument(RBACPermissionBase):
    """Allow creating patient documents."""

    permission_code = PatientDocumentPermission.CREATE
    message = "You do not have permission to create patient documents."


class CanUpdatePatientDocument(RBACPermissionBase):
    """Allow updating patient documents."""

    permission_code = PatientDocumentPermission.UPDATE
    message = "You do not have permission to update patient documents."


class CanDeletePatientDocument(RBACPermissionBase):
    """Allow deleting patient documents."""

    permission_code = PatientDocumentPermission.DELETE
    message = "You do not have permission to delete patient documents."


class CanRestorePatientDocument(RBACPermissionBase):
    """Allow restoring patient documents."""

    permission_code = PatientDocumentPermission.RESTORE
    message = "You do not have permission to restore patient documents."


class CanActivatePatientDocument(RBACPermissionBase):
    """Allow activating patient documents."""

    permission_code = PatientDocumentPermission.ACTIVATE
    message = "You do not have permission to activate patient documents."


class CanArchivePatientDocument(RBACPermissionBase):
    """Allow archiving patient documents."""

    permission_code = PatientDocumentPermission.ARCHIVE
    message = "You do not have permission to archive patient documents."


class CanCreatePatientDocumentVersion(RBACPermissionBase):
    """Allow creating document versions."""

    permission_code = PatientDocumentPermission.VERSION_CREATE
    message = "You do not have permission to create document versions."


class CanViewPatientDocumentAccessAudit(RBACPermissionBase):
    """Allow viewing document access audit records."""

    permission_code = PatientDocumentPermission.ACCESS_AUDIT
    message = "You do not have permission to view document access audit records."


__all__ = (
    "CanActivatePatientDocument",
    "CanArchivePatientDocument",
    "CanCreatePatientDocument",
    "CanCreatePatientDocumentVersion",
    "CanDeletePatientDocument",
    "CanListPatientDocuments",
    "CanRestorePatientDocument",
    "CanUpdatePatientDocument",
    "CanViewPatientDocument",
    "CanViewPatientDocumentAccessAudit",
    "PatientDocumentPermission",
)
