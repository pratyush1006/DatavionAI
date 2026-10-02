"""Workflow registrations for Patient Documents."""

from __future__ import annotations

from apps.core.workflows import workflow_registry
from apps.patient_management.patient_documents.workflows import (
    PatientDocumentAccessWorkflow,
    PatientDocumentActivationWorkflow,
    PatientDocumentArchiveWorkflow,
    PatientDocumentCreationWorkflow,
    PatientDocumentDeletionWorkflow,
    PatientDocumentRestoreWorkflow,
    PatientDocumentUpdateWorkflow,
    PatientDocumentVersionCreationWorkflow,
)

workflow_registry.register(
    name="patient_document.access",
    workflow=PatientDocumentAccessWorkflow,
)
workflow_registry.register(
    name="patient_document.create",
    workflow=PatientDocumentCreationWorkflow,
)
workflow_registry.register(
    name="patient_document.update",
    workflow=PatientDocumentUpdateWorkflow,
)
workflow_registry.register(
    name="patient_document.delete",
    workflow=PatientDocumentDeletionWorkflow,
)
workflow_registry.register(
    name="patient_document.activate",
    workflow=PatientDocumentActivationWorkflow,
)
workflow_registry.register(
    name="patient_document.archive",
    workflow=PatientDocumentArchiveWorkflow,
)
workflow_registry.register(
    name="patient_document.restore",
    workflow=PatientDocumentRestoreWorkflow,
)
workflow_registry.register(
    name="patient_document.version.create",
    workflow=PatientDocumentVersionCreationWorkflow,
)


__all__: tuple[str, ...] = ()
